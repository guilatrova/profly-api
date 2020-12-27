from dataclasses import dataclass


@dataclass
class StockInfo:
    name: str
    ticker: str
    currency: str
    current_price: float
    logo_url: str
