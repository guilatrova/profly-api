from dataclasses import dataclass


@dataclass
class CurrencyRate:
    from_currency: str
    to_currency: str
    rate: float
