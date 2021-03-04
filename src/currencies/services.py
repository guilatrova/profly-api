from .adapters import YahooRateScrapper
from .dtos import CurrencyRate


class CurrencyRateService:
    def __init__(self):
        self.scrapper = YahooRateScrapper()

    def get_currency_rate(self, from_currency: str, to_currency: str):
        rate = self.scrapper.get_rate(from_currency, to_currency)

        return CurrencyRate(from_currency, to_currency, rate)
