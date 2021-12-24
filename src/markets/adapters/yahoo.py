import logging
from typing import Iterable, Optional

import yfinance
from pandas.core.series import Series

from markets.dtos import StockHistory, StockInfo

logger = logging.getLogger(__name__)


class YahooFactory:
    """Transforms yfinance responses into objects."""

    def build_stock_info(self, payload: dict) -> StockInfo:
        mapping = {
            "name": "longName",
            "ticker": "symbol",
            "currency": "currency",
            "current_price": "ask",
            "logo_url": "logo_url",
        }
        data = {}
        for to_prop, from_prop in mapping.items():
            data[to_prop] = payload.get(from_prop)

        return StockInfo(**data)  # type: ignore

    def build_stock_history(self, ticker: str, payload: Series) -> Iterable[StockHistory]:
        for date, values in payload.iterrows():
            yield StockHistory(ticker, date, values["Open"], values["High"], values["Close"])

    def get_last_close_price(self, history: Iterable[StockHistory]) -> Optional[float]:
        for entry in history:
            return entry.close

        return None


class YahooAdapter:
    """
    Adapter that internally uses yfinance which scrapes data from
    Yahoo Finance.
    """

    def __init__(self):
        self.factory = YahooFactory()

    def get_stock_info(self, ticker_symbol: str) -> StockInfo:
        try:
            info = yfinance.Ticker(ticker_symbol).info
            logger.info(f"Got info: {info}")
        except Exception:
            logger.exception(f"Unable to get ticker '{ticker_symbol}'")
            raise
        else:
            return self.factory.build_stock_info(info)

    def get_history(self, ticker_symbol: str, period: str, interval: str) -> Iterable[StockHistory]:
        try:
            history = yfinance.Ticker(ticker_symbol).history(period, interval)
            logger.info(f"Got history: {history}")
        except Exception:
            logger.exception(f"Unable to get ticker '{ticker_symbol}'")
            return []
        else:
            return self.factory.build_stock_history(ticker_symbol, history)

    def get_last_price(self, ticker_symbol: str) -> Optional[float]:
        try:
            history = yfinance.Ticker(ticker_symbol).history("1d")
            logger.info(f"Got history: {history}")
        except Exception:
            logger.exception(f"Unable to get ticker '{ticker_symbol}'")
            return None
        else:
            stock_history = self.factory.build_stock_history(ticker_symbol, history)
            return self.factory.get_last_close_price(stock_history)
