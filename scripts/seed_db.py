from sqlmodel import Session

from app.db.schema import ConversionRate
from app.db.session import engine

sample_rates = [
    {"from_currency": "USD", "to_currency": "EUR", "rate": 0.91},
    {"from_currency": "EUR", "to_currency": "USD", "rate": 1.10},
    {"from_currency": "USD", "to_currency": "JPY", "rate": 150.0},
    {"from_currency": "GBP", "to_currency": "USD", "rate": 1.28},
    {"from_currency": "USD", "to_currency": "GBP", "rate": 0.78},
]


def main():
    with Session(engine) as session:
        for entry in sample_rates:
            rate = ConversionRate(**entry)
            session.add(rate)
        session.commit()
        session.close()
    print("Seeded exchange rates.")


if __name__ == "__main__":
    main()
