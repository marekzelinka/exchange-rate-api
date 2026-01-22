from sqlmodel import Session

from app.models import ConversionRate
from app.services.exchange_rate_service import ExchangeRateService


def test_service_convert_valid(session: Session) -> None:
    session.add(ConversionRate(from_currency="USD", to_currency="JPY", rate=150))
    session.commit()

    service = ExchangeRateService(session)

    conversion_result = service.convert("usd", "jpy", 10)
    assert conversion_result is not None
    assert conversion_result.rate == 150
    assert conversion_result.result == 1500


def test_service_convert_invalid_currency(session: Session) -> None:
    service = ExchangeRateService(session)

    result = service.convert("AAA", "BBB", 10)
    assert result is None
