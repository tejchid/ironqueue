from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import redis

from app.db.session import SessionLocal
from app.models.job import Job, JobStatus
from app.schemas.jobs import JobCreate, JobRead
from app.core.config import settings

router = APIRouter()
r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/jobs", response_model=JobRead)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    j = Job(
        type=job.type,
        payload=job.payload,
        max_attempts=job.max_attempts,
    )
    db.add(j)
    db.commit()
    db.refresh(j)

    r.lpush("job_queue", j.id)
    return j


@router.get("/jobs/{job_id}", response_model=JobRead)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404)
    return job


@router.get("/jobs", response_model=list[JobRead])
def list_jobs(status: JobStatus, db: Session = Depends(get_db)):
    return db.query(Job).filter(Job.status == status).all()
