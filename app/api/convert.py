from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.core.limiter import limiter
from app.db.session import SessionDep
from app.services.exchange_rate_service import ExchangeRateService

router = APIRouter()


def get_exchange_rate_service(session: SessionDep):
    yield ExchangeRateService(session)


@router.get("")
@limiter.limit("5/minute")
async def convert(
    request: Request,
    from_currency: Annotated[str, Query(max_length=3, min_length=3)],
    to_currency: Annotated[str, Query(max_length=3, min_length=3)],
    amount: Annotated[float, Query(gt=0)],
    service: Annotated[ExchangeRateService, Depends(get_exchange_rate_service)],
):
    try:
        return service.convert(from_currency, to_currency, amount)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
