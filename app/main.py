from fastapi import FastAPI
from app.api.routes_jobs import router

app = FastAPI(title="IronQueue")
app.include_router(router)
