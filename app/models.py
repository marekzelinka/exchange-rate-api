from datetime import datetime

from sqlmodel import Field, SQLModel


class ConversionRate(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    from_currency: str = Field(min_length=3, max_length=3)
    to_currency: str = Field(min_length=3, max_length=3)
    rate: float = Field(gt=0)
    timestamp: datetime = Field(default_factory=datetime.now)


class Conversion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    from_currency: str = Field(min_length=3, max_length=3)
    to_currency: str = Field(min_length=3, max_length=3)
    amount: float
    result: float
    timestamp: datetime = Field(default_factory=datetime.now)


class ConversionResult(SQLModel):
    rate: float
    result: float
