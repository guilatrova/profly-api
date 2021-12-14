import csv

from .models import StockTransaction


class TransactionsCSVDataFactory:
    def write_data(self, user, http_response):
        writer = csv.writer(http_response)
        writer.writerow(
            [
                "Date Time",
                "Stock",
                "Strike Price",
                "Action",
                "Units",
                "Value",
                "Emotion",
            ]
        )

        for t in StockTransaction.objects.filter(user=user).prefetch_related("stock"):
            writer.writerow(
                [
                    str(t.performed_at),
                    t.stock.ticker,
                    t.strike_price,
                    "buy" if t.units > 0 else "sell",
                    t.units,
                    t.value,
                    t.emotion,
                ]
            )
