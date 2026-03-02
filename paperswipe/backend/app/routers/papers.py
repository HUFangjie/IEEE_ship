from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Paper, Summary, Swipe

router = APIRouter(prefix="/api", tags=["papers"])


@router.get("/papers/queue")
def queue(publication: str = "TIFS", query: str = "", only_unswiped: int = 1, limit: int = 30, db: Session = Depends(get_db)):
    q = db.query(Paper).filter(Paper.publication == publication)
    if query:
        q = q.filter(Paper.keywords == query)
    papers = q.order_by(Paper.created_at.desc()).limit(limit * 2).all()
    out = []
    for p in papers:
        if only_unswiped and db.query(Swipe).filter(Swipe.paper_id == p.id).first():
            continue
        s = db.query(Summary).filter(Summary.paper_id == p.id).first()
        out.append(
            {
                "id": p.id,
                "title": p.title,
                "authors": json.loads(p.authors or "[]"),
                "abstract": p.abstract,
                "doi": p.doi,
                "year": p.year,
                "xplore_url": p.xplore_url,
                "pdf_url": p.pdf_url,
                "is_oa": p.is_oa,
                "summary": json.loads(s.summary_json) if s else None,
                "summary_md": s.summary_md if s else "Summarizing...",
            }
        )
        if len(out) >= limit:
            break
    return out


@router.get("/liked")
def liked(publication: str = "TIFS", tag: str = "", year: int | None = None, db: Session = Depends(get_db)):
    rows = db.query(Swipe, Paper).join(Paper, Swipe.paper_id == Paper.id).filter(Swipe.decision == "LIKED", Paper.publication == publication)
    if year:
        rows = rows.filter(Paper.year == year)
    result = []
    for swipe, paper in rows.all():
        tags = swipe.tags or ""
        if tag and tag not in tags:
            continue
        result.append({
            "paper_id": paper.id,
            "title": paper.title,
            "doi": paper.doi,
            "year": paper.year,
            "tags": tags,
            "url": paper.xplore_url,
        })
    return result
