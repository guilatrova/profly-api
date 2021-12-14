from django.conf import settings
from django.db import models
from django.utils import timezone

from profly.models import MonetaryField


class Wallet(models.Model):
    name = models.CharField(max_length=45, default="default")
    currency = models.CharField(max_length=10, default="USD")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "wallets"


class SavingTransaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)

    value = MonetaryField()
    notes = models.CharField(null=True, max_length=255)

    performed_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "saving_transactions"
        ordering = ["-performed_at"]
