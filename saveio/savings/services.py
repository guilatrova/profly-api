import logging
from typing import Optional

import yfinance

from .dtos import StockInfo

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

    def get_from_ticker(self, ticker_symbol: str) -> Optional[StockInfo]:
        try:
            info = yfinance.Ticker(ticker_symbol).info
            logger.info(f"Got {info}")
        except Exception:
            logger.exception(f"Unable to get ticker '{ticker_symbol}'")
        else:
            return self._build_stock_info(info)
