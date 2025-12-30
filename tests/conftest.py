import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from app.db.session import get_session
from app.main import app


@pytest.fixture(name="session")
def session_fixture():
    DATABASE_URL = "sqlite:///:memory:"
    connect_args = {"check_same_thread": False}
    engine = create_engine(
        DATABASE_URL, connect_args=connect_args, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
