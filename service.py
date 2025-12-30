from decimal import Decimal

from fastapi import HTTPException

# Exchange rates
RATES = {
    ("USD", "EUR"): Decimal("0.91"),
    ("EUR", "USD"): Decimal("1.10"),
    ("USD", "JPY"): Decimal("150.0"),
}


class ExchangeRateService:
    def convert(self, from_currency: str, to_currency: str, amount: Decimal) -> Decimal:
        key = (from_currency.upper(), to_currency.upper())
        rate = RATES.get(key)

        if rate is None:
            raise HTTPException(status_code=400, detail="Exchange rate not available")

        print(f"Using rate {rate}")
        return amount * rate
