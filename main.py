from decimal import Decimal
from typing import Annotated

import uvicorn
from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

# Exchange rates
RATES = {
    ("USD", "EUR"): Decimal("0.91"),
    ("EUR", "USD"): Decimal("1.10"),
    ("USD", "JPY"): Decimal("150.0"),
}


@app.get("/convert")
def convert(
    from_currency: Annotated[str, Query(max_length=3, min_length=3)],
    to_currency: Annotated[str, Query(max_length=3, min_length=3)],
    amount: Annotated[Decimal, Query(gt=0)],
):
    key = (from_currency.upper(), to_currency.upper())
    rate = RATES.get(key)

    if rate is None:
        raise HTTPException(status_code=400, detail="Exchange rate not available")

    print(f"Using rate {rate}")
    return {"result": amount * rate}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
