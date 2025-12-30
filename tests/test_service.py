from sqlmodel import Session

from app.db.schema import ConversionRate
from app.services.exchange_rate_service import ExchangeRateService


def test_service_convert_valid(session: Session):
    session.add(ConversionRate(from_currency="USD", to_currency="JPY", rate=150))
    session.commit()

    service = ExchangeRateService(session)
    result = service.convert("usd", "jpy", 10)
    assert result["rate"] == 150
    assert result["result"] == 1500


def test_service_convert_invalid_currency(session: Session):
    service = ExchangeRateService(session)
    try:
        service.convert("AAA", "BBB", 10)
        assert False, "Expected HTTPException"
    except Exception as e:
        assert "Exchange rate not available" in str(e)
