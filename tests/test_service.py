from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import ConversionRate
from app.service import ExchangeRateService


def test_service_convert_valid(db_session: Session):
    db_session.add(ConversionRate(from_currency="USD", to_currency="JPY", rate=150))
    db_session.commit()

    service = ExchangeRateService(db_session)
    result = service.convert("usd", "jpy", Decimal("10.0"))
    assert result["rate"] == 150
    assert result["result"] == 1500


def test_service_convert_invalid_currency(db_session: Session):
    service = ExchangeRateService(db_session)
    try:
        service.convert("AAA", "BBB", Decimal("10.0"))
        assert False, "Expected HTTPException"
    except Exception as e:
        assert "Exchange rate not available" in str(e)
