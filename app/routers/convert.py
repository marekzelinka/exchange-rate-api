from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.core.limiter import limiter
from app.db.session import SessionDep
from app.services.exchange_rate_service import ExchangeRateService

router = APIRouter(prefix="/convert", tags=["convert"])


def get_exchange_rate_service(session: SessionDep):
    yield ExchangeRateService(session)


@router.get("/")
@limiter.limit("5/minute")
async def read_exchange_rate(
    request: Request,
    from_currency: Annotated[str, Query(max_length=3, min_length=3)],
    to_currency: Annotated[str, Query(max_length=3, min_length=3)],
    amount: Annotated[float, Query(gt=0)],
    service: Annotated[ExchangeRateService, Depends(get_exchange_rate_service)],
):
    result = service.convert(from_currency, to_currency, amount)
    if not result:
        raise HTTPException(status_code=404, detail="Exchange rate not available")
    return result
