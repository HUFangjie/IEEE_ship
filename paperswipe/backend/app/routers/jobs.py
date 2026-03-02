from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Job

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.get("")
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).order_by(Job.created_at.desc()).limit(20).all()
    return [{"id": j.id, "type": j.type, "status": j.status, "total": j.total, "done": j.done, "error": j.error, "created_at": j.created_at, "updated_at": j.updated_at} for j in jobs]


@router.get("/{job_id}")
def get_job(job_id: str, db: Session = Depends(get_db)):
    j = db.get(Job, job_id)
    if not j:
        return {"error": "not found"}
    return {
        "id": j.id,
        "status": j.status,
        "total": j.total,
        "done": j.done,
        "error": j.error,
    }
