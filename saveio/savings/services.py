import logging
from typing import Iterable, Optional

import yfinance

from .dtos import StockHistory, StockInfo, StockUnitsByTicker
from .models import Transaction

logger = logging.getLogger(__name__)


class StocksMarketService:
    def _build_stock_info(self, payload: dict) -> StockInfo:
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

        return StockInfo(**data)

    def _build_stock_history(self, ticker: str, payload: dict) -> StockHistory:
        for date, values in payload.iterrows():
            yield StockHistory(
                ticker, date, values["Open"], values["High"], values["Close"]
            )

    def get_from_ticker(self, ticker_symbol: str) -> Optional[StockInfo]:
        try:
            info = yfinance.Ticker(ticker_symbol).info
            logger.info(f"Got info: {info}")
        except Exception:
            logger.exception(f"Unable to get ticker '{ticker_symbol}'")
        else:
            return self._build_stock_info(info)

    def get_history_from_ticker(self, ticker_symbol: str, period: str = "1d"):
        try:
            history = yfinance.Ticker(ticker_symbol).history(period)
            logger.info(f"Got history: {history}")
        except Exception:
            logger.exception(f"Unable to get ticker '{ticker_symbol}'")
        else:
            return self._build_stock_history(ticker_symbol, history)


class ChartDataFactory:
    def __init__(self):
        self.market_service = StocksMarketService()

    def build_stock_units_current_value(self) -> Iterable[StockUnitsByTicker]:
        aggregated_data = Transaction.objects.aggregate_units_by_ticker()
        for units_by_ticker in aggregated_data:
            ticker = units_by_ticker["ticker"]
            history = next(self.market_service.get_history_from_ticker(ticker))
            yield StockUnitsByTicker(
                ticker, units_by_ticker["total_units"], history.close
            )
