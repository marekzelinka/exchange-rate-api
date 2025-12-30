import logging
from datetime import datetime
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Conversion, ConversionRate


class ExchangeRateService:
    def __init__(self, db: Session) -> None:
        self.db: Session = db

    def convert(self, from_currency: str, to_currency: str, amount: Decimal) -> dict:
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        rate_entry = (
            self.db.query(ConversionRate)
            .filter_by(from_currency=from_currency, to_currency=to_currency)
            .order_by(ConversionRate.timestamp.desc())
            .first()
        )

        if not rate_entry or rate_entry.rate <= 0:
            raise HTTPException(status_code=404, detail="Exchange rate not available")

        logging.info(f"Using rate {rate_entry.rate}")
        result = Decimal(amount) * rate_entry.rate

        conversion = Conversion(
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
            result=result,
            timestamp=datetime.now(),
        )
        self.db.add(conversion)
        self.db.commit()

        return {"rate": rate_entry.rate, "result": result}
