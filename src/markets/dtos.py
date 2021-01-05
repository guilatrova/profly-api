import math
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

ROUND_DIGITS = 2


def _handle_nan(raw, do_round=True):
    if math.isnan(raw):
        return None

    if do_round:
        return round(raw, ROUND_DIGITS)

    return raw


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
    open: Optional[float]
    high: Optional[float]
    close: Optional[float]

    def __post_init__(self):
        self.open = _handle_nan(self.open)
        self.high = _handle_nan(self.high)
        self.close = _handle_nan(self.close)


@dataclass
class StockUnitsByTicker:
    ticker: str
    total_units: float
    close_price: float
    total_value: float = field(init=False)

    def __post_init__(self):
        self.close_price = round(self.close_price or 0, ROUND_DIGITS)
        self.total_value = self.close_price * self.total_units


@dataclass
class OwnedStockSummary:
    """Represents how much you own and
    average price you paid/sold
    """

    ticker: str
    units: float
    average_buy_price: float
    average_sell_price: float
