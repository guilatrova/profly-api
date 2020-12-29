from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Manager, Sum


class TransactionManager(Manager):
    def aggregate_units_by_ticker(self):
        return (
            self.values(ticker=F("stock__ticker"))
            .order_by("stock_id")
            .annotate(total_units=Sum("units"))
            .filter(total_units__gt=0)
        )


class StockManager(Manager):
    def find(self, ticker: str):
        try:
            stock = self.get(ticker=ticker)
        except ObjectDoesNotExist:
            stock = None

        return stock
