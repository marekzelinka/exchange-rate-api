from collections.abc import Generator
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from app.core.limiter import limiter
from app.deps import SessionDep
from app.models import ConversionResult
from app.services.exchange_rate_service import ExchangeRateService

router = APIRouter(prefix="/convert", tags=["convert"])


def get_exchange_rate_service(session: SessionDep) -> Generator[ExchangeRateService]:
    yield ExchangeRateService(session)


@router.get("/")
@limiter.limit("5/minute")
async def read_exchange_rate(
    *,
    request: Request,  # noqa: ARG001 slowapi.Limiter need this
    service: Annotated[ExchangeRateService, Depends(get_exchange_rate_service)],
    from_currency: Annotated[str, Query(max_length=3, min_length=3)],
    to_currency: Annotated[str, Query(max_length=3, min_length=3)],
    amount: Annotated[float, Query(gt=0)],
) -> ConversionResult:
    conversion_result = service.convert(from_currency, to_currency, amount)
    if not conversion_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exchange rate not found"
        )

    return conversion_result
