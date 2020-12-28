from dataclasses import dataclass
from datetime import datetime


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

    @property
    def total_value(self):
        return self.close_price * self.total_units
