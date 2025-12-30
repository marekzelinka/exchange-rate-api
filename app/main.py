from fastapi import FastAPI

from app.api import router
from app.db.session import create_db_and_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(router)
