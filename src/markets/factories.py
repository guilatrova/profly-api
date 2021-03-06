from typing import Iterable

from markets.dtos import OwnedStockSummary, StockHistory, StockUnitsByTicker
from savings.models import Transaction

from .services import StocksMarketService


class ChartDataFactory:
    def __init__(self, service=None):
        self.market_service = service or StocksMarketService()

    def build_stock_units_current_value(self, user) -> Iterable[StockUnitsByTicker]:
        aggregated_data = Transaction.objects.aggregate_units_by_ticker(user)

        for units_by_ticker in aggregated_data:
            ticker = units_by_ticker["ticker"]
            history = next(self.market_service.get_history(ticker))

            yield StockUnitsByTicker(
                ticker, units_by_ticker["total_units"], history.close
            )

    def build_stock_line_factory(
        self, ticker_symbol: str, period: str, interval: str
    ) -> Iterable[StockHistory]:
        """
        period: data period to download (either use period parameter or use start and
        end) Valid periods are:
        “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”

        interval: data interval (1m data is only for available for last 7 days, and
        data interval <1d for the last 60 days) Valid intervals are:
        “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”,
        “3mo”
        """
        return self.market_service.get_history(ticker_symbol, period, interval)

    def build_owned_stock_summary(self, user, ticker_symbol: str) -> OwnedStockSummary:
        avg_data = Transaction.objects.aggregate_avg_units_price_by_ticker(user).get(
            ticker=ticker_symbol
        )
        return OwnedStockSummary(
            ticker=ticker_symbol,
            units=avg_data["total_units"],
            average_buy_price=avg_data["avg_buy_price"],
            average_sell_price=avg_data["avg_sell_price"],
        )
