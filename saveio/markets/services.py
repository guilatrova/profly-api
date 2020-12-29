from typing import Iterable, Optional

from savings.models import Stock

from .adapters import YahooAdapter
from .dtos import StockHistory, StockInfo


class StocksMarketService:
    def __init__(self, adapter=None):
        self.adapter = adapter or YahooAdapter()

    def _handle_new_stock(self, info: Optional[StockInfo]):
        if info:
            return Stock.objects.create(
                ticker=info.ticker,
                name=info.name,
                currency=info.currency,
                logo_url=info.logo_url,
            )

    def _get_stock_info_from_source(self, ticker_symbol: str) -> Optional[StockInfo]:
        return self.adapter.get_stock_info(ticker_symbol)

    def get_stock(self, ticker_symbol: str) -> Optional[Stock]:
        stock = Stock.objects.find(ticker_symbol)
        missing_in_database = not stock

        if missing_in_database:
            info = self._get_stock_info_from_source(ticker_symbol)
            stock = self._handle_new_stock(info)

        return stock

    def get_stock_info(self, ticker_symbol: str) -> StockInfo:
        stock = Stock.objects.find(ticker_symbol)
        missing_in_database = not stock

        if missing_in_database:
            info = self._get_stock_info_from_source(ticker_symbol)
            stock = self._handle_new_stock(info)
            price = info.current_price
        else:
            price = self.adapter.get_last_price(ticker_symbol)

        return StockInfo(
            stock.name, stock.ticker, stock.currency, price, stock.logo_url
        )

    def get_history(
        self, ticker_symbol: str, period: str = "1d", interval: str = "1d"
    ) -> Iterable[StockHistory]:
        return self.adapter.get_history(ticker_symbol, period, interval)
