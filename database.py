from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config
from models import Base

DB_URL = config.database_url
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ensure tables are created
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
