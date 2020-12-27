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
