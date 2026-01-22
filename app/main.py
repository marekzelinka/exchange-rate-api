import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import config
from app.core.db import create_db_and_tables
from app.deps import SessionDep
from app.routers import convert

logging.basicConfig(
    level=config.log_level,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

# Set all CORS enabled origins
if config.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,  # ty:ignore[invalid-argument-type]
        allow_origins=config.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(convert.router)


@app.get("/health", tags=["status"])
async def read_health_status(*, _session: SessionDep) -> dict:
    return {"status": "OK"}
