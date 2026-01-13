import time
from datetime import datetime, timedelta
import redis
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.job import Job, JobStatus
from app.core.config import settings

TIMEOUT = 30
r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

while True:
    db: Session = SessionLocal()
    cutoff = datetime.utcnow() - timedelta(seconds=TIMEOUT)

    stuck = (
        db.query(Job)
        .filter(
            Job.status == JobStatus.RUNNING,
            Job.started_at < cutoff
        )
        .all()
    )

    for job in stuck:
        if job.attempts < job.max_attempts:
            job.attempts += 1
            job.status = JobStatus.QUEUED
            job.started_at = None
            r.lpush("job_queue", job.id)
        else:
            job.status = JobStatus.FAILED

    db.commit()
    db.close()
    time.sleep(10)
