from .adapters import YahooAdapter


class StocksMarketService:
    def __init__(self, adapter=None):
        self.adapter = adapter or YahooAdapter()

    def get_stock_info(self, ticker_symbol: str):
        return self.adapter.get_stock_info(ticker_symbol)

    def get_history(self, ticker_symbol: str, period: str = "1d"):
        return self.adapter.get_history(ticker_symbol, period)
