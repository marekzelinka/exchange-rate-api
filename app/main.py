from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api import convert, health
from .core.logging import setup_logging
from .db.session import create_db_and_tables

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(convert.router, prefix="/convert")
app.include_router(health.router, prefix="/health")
