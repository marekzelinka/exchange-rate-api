import logging
from datetime import datetime

from sqlmodel import Session, and_, desc, select

from app.models import Conversion, ConversionRate, ConversionResult


class ExchangeRateService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def convert(
        self, from_currency: str, to_currency: str, amount: float
    ) -> ConversionResult | None:
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
        entry = results.first()

        if not entry or entry.rate <= 0:
            return None

        logging.info(f"Using rate {entry.rate}")
        result = amount * entry.rate

        conversion = Conversion(
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
            result=result,
            timestamp=datetime.now(),
        )

        self.session.add(conversion)
        self.session.commit()

        return ConversionResult(rate=entry.rate, result=result)
