from django.db import models


class MonetaryField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs["max_digits"] = 19
        kwargs["decimal_places"] = 10
        super().__init__(*args, **kwargs)


class Stock(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10)


class Transaction(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)
    value = MonetaryField()
    strike_price = MonetaryField()
    units = models.IntegerField()

    created_at = models.DateField(auto_now=True)
