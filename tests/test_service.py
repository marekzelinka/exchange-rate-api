from sqlmodel import Session

from app.db.schema import ConversionRate
from app.services.exchange_rate_service import ExchangeRateService


def test_service_convert_valid(session: Session):
    session.add(ConversionRate(from_currency="USD", to_currency="JPY", rate=150))
    session.commit()

    service = ExchangeRateService(session)
    result = service.convert("usd", "jpy", 10)
    assert result is not None
    assert result["rate"] == 150
    assert result["result"] == 1500


def test_service_convert_invalid_currency(session: Session):
    service = ExchangeRateService(session)
    result = service.convert("AAA", "BBB", 10)
    assert result is None
