from typing import Iterable

from markets.dtos import StockUnitsByTicker
from savings.models import Transaction

from .services import StocksMarketService


class ChartDataFactory:
    def __init__(self, service=None):
        self.market_service = service or StocksMarketService()

    def build_stock_units_current_value(self) -> Iterable[StockUnitsByTicker]:
        aggregated_data = Transaction.objects.aggregate_units_by_ticker()

        for units_by_ticker in aggregated_data:
            ticker = units_by_ticker["ticker"]
            history = next(self.market_service.get_history(ticker))

            yield StockUnitsByTicker(
                ticker, units_by_ticker["total_units"], history.close
            )
