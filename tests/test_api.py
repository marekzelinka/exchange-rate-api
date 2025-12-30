from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import ConversionRate


def test_convert_success(client: TestClient, db_session: Session):
    db_session.add(ConversionRate(from_currency="USD", to_currency="EUR", rate=0.9))
    db_session.commit()

    r = client.get("/convert?from_currency=USD&to_currency=EUR&amount=100")
    assert r.status_code == 200
    data = r.json()
    assert data["rate"] == 0.9
    assert data["result"] == 90.0


def test_convert_missing_rate(client: TestClient):
    r = client.get("/convert?from_currency=GBP&to_currency=JPY&amount=50")
    assert r.status_code == 500
    assert "Exchange rate not available" in r.json()["detail"]
