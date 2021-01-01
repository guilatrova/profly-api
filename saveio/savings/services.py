import csv

from .models import Transaction


class TransactionsCSVDataFactory:
    def write_data(self, http_response):
        writer = csv.writer(http_response)
        writer.writerow(
            ["Date Time", "Stock", "Strike Price", "Action", "Units", "Value"]
        )

        for t in Transaction.objects.all().prefetch_related("stock"):
            writer.writerow(
                [
                    str(t.performed_at),
                    t.stock.ticker,
                    t.strike_price,
                    "buy" if t.units > 0 else "sell",
                    t.units,
                    t.value,
                ]
            )