from __future__ import annotations

import asyncio
import json
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Paper, Summary, Swipe
from ..schemas import SwipeRequest
from ..services.library_writer import write_liked_bundle
from ..settings import get_settings

router = APIRouter(prefix="/api/swipe", tags=["swipe"])


def now():
    return datetime.utcnow().isoformat()


async def like_side_effect(paper: Paper, summary: Summary | None):
    settings = get_settings()
    paper_dict = {
        "id": paper.id,
        "title": paper.title,
        "authors": json.loads(paper.authors or "[]"),
        "abstract": paper.abstract,
        "doi": paper.doi,
        "year": paper.year,
        "xplore_url": paper.xplore_url,
        "pdf_url": paper.pdf_url,
        "is_oa": paper.is_oa,
    }
    summary_json = json.loads(summary.summary_json) if summary else {}
    summary_md = summary.summary_md if summary else ""
    await write_liked_bundle(settings.library_path, paper_dict, summary_json, summary_md)


@router.post("")
async def swipe(req: SwipeRequest, db: Session = Depends(get_db)):
    rec = Swipe(
        id=str(uuid.uuid4()),
        paper_id=req.paper_id,
        decision=req.decision,
        notes=req.notes,
        tags=",".join(req.tags),
        swiped_at=now(),
    )
    db.add(rec)
    db.commit()

    if req.decision == "LIKED":
        paper = db.get(Paper, req.paper_id)
        summary = db.query(Summary).filter(Summary.paper_id == req.paper_id).first()
        asyncio.create_task(like_side_effect(paper, summary))
    return {"ok": True}
