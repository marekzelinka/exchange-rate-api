from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import ConversionRate


def test_convert_success(client: TestClient, session: Session) -> None:
    session.add(ConversionRate(from_currency="USD", to_currency="EUR", rate=0.9))
    session.commit()

    response = client.get("/convert?from_currency=USD&to_currency=EUR&amount=100")
    assert response.status_code == 200

    data = response.json()
    assert data["rate"] == 0.9
    assert data["result"] == 90.0


def test_convert_missing_rate(client: TestClient) -> None:
    response = client.get("/convert?from_currency=GBP&to_currency=JPY&amount=50")
    assert response.status_code == 404
    assert "Exchange rate not found" in response.json()["detail"]
