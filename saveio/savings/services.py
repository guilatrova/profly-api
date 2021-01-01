import csv
from datetime import date

from .models import Transaction


class TransactionsCSVDataFactory:
    def __init__(self, http_response):
        suffix = str(date.today())
        self.http_response = http_response
        self.http_response[
            "Content-Disposition"
        ] = f'attachment; filename="transactions{suffix}.csv"'

    def write_data(self):
        writer = csv.writer(self.http_response)
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
