from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from service import ExchangeRateService

router = APIRouter()


def get_exchange_rate_service(session: Annotated[Session, Depends(get_db)]):
    yield ExchangeRateService(session)


@router.get("/convert")
def convert(
    from_currency: Annotated[str, Query(max_length=3, min_length=3)],
    to_currency: Annotated[str, Query(max_length=3, min_length=3)],
    amount: Annotated[Decimal, Query(gt=0)],
    service: Annotated[ExchangeRateService, Depends(get_exchange_rate_service)],
):
    return service.convert(from_currency, to_currency, amount)
