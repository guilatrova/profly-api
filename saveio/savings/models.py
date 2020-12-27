from django.db import models
from django.utils import timezone


class MonetaryField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs["max_digits"] = 19
        kwargs["decimal_places"] = 10
        super().__init__(*args, **kwargs)


class Stock(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10, unique=True)


class Transaction(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)
    strike_price = MonetaryField()
    units = models.IntegerField()

    performed_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now=True)

    @property
    def value(self):
        return self.strike_price * self.units
