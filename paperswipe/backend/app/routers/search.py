from __future__ import annotations

import asyncio
import json
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import SessionLocal, get_db
from ..models import Job, Paper, Summary
from ..schemas import SearchRequest
from ..services.ieee_client import IEEEClient
from ..services.summarizer import default_summary, summarize_kimi, summarize_openai
from ..settings import get_settings

router = APIRouter(prefix="/api/search", tags=["search"])


def now():
    return datetime.utcnow().isoformat()


def dedup_key(item: dict) -> str:
    return item.get("doi") or f"{item.get('title','')}_{item.get('year','')}"


async def process_search_job(job_id: str, req: SearchRequest):
    db = SessionLocal()
    try:
        settings = get_settings()
        client = IEEEClient(settings.ieee_api_key)
        job = db.get(Job, job_id)
        job.status = "RUNNING"
        db.commit()

        papers = await client.search(req.query, req.publication, req.year_from, req.year_to, req.limit)
        job.total = len(papers)
        db.commit()

        for item in papers:
            exists = db.query(Paper).filter((Paper.doi == item.get("doi")) if item.get("doi") else (Paper.title == item["title"]) & (Paper.year == item["year"])).first()
            if exists:
                job.done += 1
                db.commit()
                continue
            pid = str(uuid.uuid4())
            paper = Paper(
                id=pid,
                keywords=req.query,
                created_at=now(),
                updated_at=now(),
                **item,
                authors=json.dumps(item.get("authors", []), ensure_ascii=False),
            )
            db.add(paper)
            db.flush()

            payload = {
                "title": item["title"],
                "abstract": item.get("abstract") or "",
                "venue": req.publication,
                "year": item["year"],
                "user_query": req.query,
            }
            try:
                if settings.llm_provider == "kimi":
                    model = "moonshot-v1-8k"
                    summary_json, summary_md = await summarize_kimi(settings.kimi_api_key, model, payload)
                elif settings.llm_provider == "openai":
                    model = "gpt-4o-mini"
                    summary_json, summary_md = await summarize_openai(settings.openai_api_key, model, payload)
                else:
                    model = "gemini-1.5-flash"
                    summary_json = default_summary(req.query)
                    summary_md = "Gemini is optional in MVP and not wired yet."
            except Exception:
                model = "fallback"
                summary_json = default_summary(req.query)
                summary_md = "Summarization failed."
            db.add(
                Summary(
                    id=str(uuid.uuid4()),
                    paper_id=pid,
                    provider=settings.llm_provider,
                    model=model,
                    summary_json=json.dumps(summary_json, ensure_ascii=False),
                    summary_md=summary_md,
                    created_at=now(),
                )
            )
            job.done += 1
            job.updated_at = now()
            db.commit()

        job.status = "DONE"
        db.commit()
    except Exception as exc:
        job = db.get(Job, job_id)
        if job:
            job.status = "ERROR"
            job.error = str(exc)
            db.commit()
    finally:
        db.close()


@router.post("")
async def search(req: SearchRequest, db: Session = Depends(get_db)):
    job = Job(
        id=str(uuid.uuid4()),
        type="FETCH",
        status="PENDING",
        total=req.limit,
        done=0,
        created_at=now(),
        updated_at=now(),
    )
    db.add(job)
    db.commit()
    asyncio.create_task(process_search_job(job.id, req))
    return {"job_id": job.id, "estimated": req.limit}
