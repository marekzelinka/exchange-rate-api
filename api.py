from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from service import ExchangeRateService

router = APIRouter()


@router.get("/convert")
def convert(
    from_currency: Annotated[str, Query(max_length=3, min_length=3)],
    to_currency: Annotated[str, Query(max_length=3, min_length=3)],
    amount: Annotated[Decimal, Query(gt=0)],
    service: Annotated[ExchangeRateService, Depends()],
):
    result = service.convert(from_currency, to_currency, amount)

    return {"result": result}
