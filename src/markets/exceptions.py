class MarketsException(Exception):
    """Represents any exception caused by a third-party integration to retrieve data"""


class UnableToGetHistory(MarketsException):
    def __init__(self, ticker_symbol) -> None:
        msg = f"Unable to get ticker '{ticker_symbol}'"
        super().__init__(msg)
