from decimal import Decimal

from django.db.models import Manager, Sum
from django.db.models.functions import Coalesce

DEFAULT_ZERO = Decimal(0)


class SavingTransactionManager(Manager):
    def aggregate_wallet_current_value(self, wallet) -> Decimal:
        aggregated = self.filter(wallet=wallet).annotate(
            total_value=Coalesce(Sum("value"), DEFAULT_ZERO)
        )
        if instance := aggregated.first():
            return instance.total_value

        return DEFAULT_ZERO


class WalletManager(Manager):
    def get_default_wallet(self, user):
        wallet, _ = self.get_or_create(
            user=user,
            name="default",
        )

        return wallet
