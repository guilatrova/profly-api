from decimal import Decimal

from django.db.models import Manager, Sum

DEFAULT_ZERO = Decimal(0)


class SavingTransactionManager(Manager):
    def aggregate_wallet_current_value(self, wallet) -> Decimal:
        aggregated = self.filter(wallet=wallet).values("wallet").aggregate(total_value=Sum("value"))

        return aggregated["total_value"]


class WalletManager(Manager):
    def get_default_wallet(self, user):
        wallet, _ = self.get_or_create(
            user=user,
            name="default",
        )

        return wallet
