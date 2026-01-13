import time
from datetime import datetime
import redis
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.job import Job, JobStatus
from app.core.config import settings

r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

while True:
    _, job_id = r.blpop("job_queue")
    db: Session = SessionLocal()

    try:
        job = (
            db.query(Job)
            .filter(
                Job.id == int(job_id),
                Job.status == JobStatus.QUEUED
            )
            .first()
        )

        if not job:
            continue

        job.status = JobStatus.RUNNING
        job.started_at = datetime.utcnow()
        db.commit()

        # simulate work
        time.sleep(2)

        job.status = JobStatus.COMPLETED
        job.finished_at = datetime.utcnow()
        db.commit()

    except Exception as e:
        job.attempts += 1
        job.last_error = str(e)

        if job.attempts < job.max_attempts:
            job.status = JobStatus.QUEUED
            job.started_at = None
            r.lpush("job_queue", job.id)
        else:
            job.status = JobStatus.FAILED

        db.commit()

    finally:
        db.close()
