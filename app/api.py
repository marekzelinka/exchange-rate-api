from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from app.database import get_db
from app.service import ExchangeRateService

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


def get_exchange_rate_service(session: Annotated[Session, Depends(get_db)]):
    yield ExchangeRateService(session)


@router.get("/convert")
@limiter.limit("5/minute")
def convert(
    request: Request,
    from_currency: Annotated[str, Query(max_length=3, min_length=3)],
    to_currency: Annotated[str, Query(max_length=3, min_length=3)],
    amount: Annotated[Decimal, Query(gt=0)],
    service: Annotated[ExchangeRateService, Depends(get_exchange_rate_service)],
):
    try:
        return service.convert(from_currency, to_currency, amount)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
def health():
    return {"status": "OK"}
