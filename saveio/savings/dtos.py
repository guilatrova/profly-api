from dataclasses import dataclass, field
from datetime import datetime

ROUND_DIGITS = 2


@dataclass
class StockInfo:
    name: str
    ticker: str
    currency: str
    current_price: float
    logo_url: str
    timestamp: datetime = datetime.utcnow()


@dataclass
class StockHistory:
    ticker: str
    date: str
    open: float
    high: float
    close: float


@dataclass
class StockUnitsByTicker:
    ticker: str
    total_units: float
    close_price: float
    total_value: float = field(init=False)

    def __post_init__(self):
        self.close_price = round(self.close_price, ROUND_DIGITS)
        self.total_value = self.close_price * self.total_units
