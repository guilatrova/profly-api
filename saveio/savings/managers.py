from django.db.models import F, Manager, Sum


class TransactionManager(Manager):
    def aggregate_units_by_ticker(self):
        return (
            self.values(ticker=F("stock__ticker"))
            .order_by("stock_id")
            .annotate(total_units=Sum("units"))
            .filter(total_units__gt=0)
        )
