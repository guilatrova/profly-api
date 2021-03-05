import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

DIV_WRAPPER_ID = "quote-header-info"
RATE_SPAN_ATTRS = {"data-reactid": 32}


class YahooRateScrapper:
    def get_rate(self, from_symbol: str, to_symbol: str):
        url = f"https://finance.yahoo.com/quote/{from_symbol}{to_symbol}=X/"
        logger.info(f"Scrapping exchange rate from: {url}")
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "lxml")
        wrapper = soup.find(id=DIV_WRAPPER_ID)
        rate = wrapper.find("span", attrs=RATE_SPAN_ATTRS).text

        return float(rate)
