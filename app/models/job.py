import enum
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Enum
from sqlalchemy.sql import func
from app.db.base import Base


class JobStatus(str, enum.Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


__all__ = ["Job", "JobStatus"]


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)

    status = Column(Enum(JobStatus), nullable=False, default=JobStatus.QUEUED)

    attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)
    last_error = Column(Text)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    started_at = Column(DateTime)
    finished_at = Column(DateTime)
