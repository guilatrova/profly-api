from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, F, Manager, Q, Sum


class TransactionManager(Manager):
    def aggregate_units_by_ticker(self, user):
        return (
            self.filter(user=user)
            .values(ticker=F("stock__ticker"))
            .order_by("stock_id")
            .annotate(total_units=Sum("units"))
            .filter(total_units__gt=0)
        )

    def aggregate_avg_units_price_by_ticker(self, user):
        return (
            self.filter(user=user)
            .values(ticker=F("stock__ticker"))
            .annotate(total_units=Sum("units"))
            .annotate(avg_buy_price=Avg("strike_price", filter=Q(units__gt=0)))
            .annotate(avg_sell_price=Avg("strike_price", filter=Q(units__lte=0)))
        )


class StockManager(Manager):
    def find(self, ticker: str):
        try:
            stock = self.get(ticker=ticker)
        except ObjectDoesNotExist:
            stock = None

        return stock
