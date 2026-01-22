import logging

from sqlmodel import Session

from app.core.config import config
from app.core.db import engine
from app.models import ConversionRate

logging.basicConfig(
    level=config.log_level,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

sample_rates = [
    {"from_currency": "USD", "to_currency": "EUR", "rate": 0.91},
    {"from_currency": "EUR", "to_currency": "USD", "rate": 1.10},
    {"from_currency": "USD", "to_currency": "JPY", "rate": 150.0},
    {"from_currency": "GBP", "to_currency": "USD", "rate": 1.28},
    {"from_currency": "USD", "to_currency": "GBP", "rate": 0.78},
]


def main() -> None:
    with Session(engine) as session:
        for entry in sample_rates:
            rate = ConversionRate(**entry)

            session.add(rate)

        session.commit()
        session.close()

    logging.info("Seeded exchange rates.")


if __name__ == "__main__":
    main()
