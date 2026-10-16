from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

import httpx
from fastapi import FastAPI
from pymongo import AsyncMongoClient

from app.api.v1.router import router as v1_router
from app.db.database import get_mongo_uri, init_mongodb


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.base_dir = Path.cwd()
    app.state.httpx_client = httpx.AsyncClient()
    client = AsyncMongoClient(get_mongo_uri())
    app.state.mongodb_client = client
    app.state.mongodb_db = await init_mongodb(client)
    try:
        yield
    finally:
        await app.state.httpx_client.aclose()
        await app.state.mongodb_client.close()


app = FastAPI(
    title="Agentic Job Seeker API",
    version="0.1.0",
    description="REST API for storing resumes, matching jobs, and generating cover letters.",
    lifespan=lifespan,
)

app.include_router(v1_router, prefix="/api/v1")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Agentic Job Seeker API is running."}
