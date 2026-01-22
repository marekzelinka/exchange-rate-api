from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from app.deps import get_session
from app.main import app


@pytest.fixture(name="session")
def session_fixture() -> Generator[Session]:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient]:
    app.dependency_overrides[get_session] = lambda: session

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()
