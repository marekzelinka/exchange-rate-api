import logging
from datetime import datetime

from sqlmodel import Session, and_, desc, select

from app.db.schema import Conversion, ConversionRate


class ExchangeRateService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def convert(
        self, from_currency: str, to_currency: str, amount: float
    ) -> dict | None:
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        results = self.session.exec(
            select(ConversionRate)
            .where(
                and_(
                    ConversionRate.from_currency == from_currency,
                    ConversionRate.to_currency == to_currency,
                )
            )
            .order_by(desc(ConversionRate.timestamp))
        )
        rate_entry = results.first()

        if not rate_entry or rate_entry.rate <= 0:
            return None

        logging.info(f"Using rate {rate_entry.rate}")
        result = amount * rate_entry.rate

        conversion = Conversion(
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
            result=result,
            timestamp=datetime.now(),
        )
        self.session.add(conversion)
        self.session.commit()

        return {"rate": rate_entry.rate, "result": result}
