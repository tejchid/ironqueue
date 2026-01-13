from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@postgres:5432/jobs"
    REDIS_URL: str = "redis://redis:6379/0"

settings = Settings()
