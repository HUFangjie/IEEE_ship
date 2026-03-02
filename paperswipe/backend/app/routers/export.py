from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Paper, Swipe
from ..services.library_writer import bibtex_from_paper

router = APIRouter(prefix="/api/export", tags=["export"])


@router.post("/bib")
def export_bib(db: Session = Depends(get_db)):
    rows = db.query(Paper).join(Swipe, Swipe.paper_id == Paper.id).filter(Swipe.decision == "LIKED").all()
    text = "\n".join(
        bibtex_from_paper({
            "id": p.id,
            "title": p.title,
            "authors": __import__("json").loads(p.authors or "[]"),
            "year": p.year,
            "doi": p.doi,
            "xplore_url": p.xplore_url,
        })
        for p in rows
    )
    return {"filename": "liked.bib", "content": text}


@router.post("/csv")
def export_csv(db: Session = Depends(get_db)):
    rows = db.query(Swipe, Paper).join(Paper, Swipe.paper_id == Paper.id).filter(Swipe.decision == "LIKED").all()
    lines = ["title,doi,year,tags,url"]
    for s, p in rows:
        lines.append(f'"{p.title}","{p.doi or ""}",{p.year},"{s.tags or ""}","{p.xplore_url}"')
    return {"filename": "liked.csv", "content": "\n".join(lines)}
