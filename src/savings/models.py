from django.conf import settings
from django.db import models
from django.utils import timezone

from . import managers


class MonetaryField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs["max_digits"] = 19
        kwargs["decimal_places"] = 10
        super().__init__(*args, **kwargs)


class Stock(models.Model):
    objects = managers.StockManager()

    ticker = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    currency = models.CharField(max_length=10)
    logo_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    objects = managers.TransactionManager()

    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)
    strike_price = MonetaryField()
    units = models.FloatField()  # units can be broken in fractions

    performed_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    emotion = models.CharField(null=True, max_length=60)
    notes = models.CharField(null=True, max_length=255)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )

    @property
    def value(self):
        modifier = 1 if self.units > 0 else -1
        return float(self.strike_price) * self.units * modifier

    class Meta:
        ordering = ["-performed_at"]
