import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Wallet

logger = logging.getLogger(__name__)


@receiver(
    post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="user-default-wallet"
)
def create_default_wallet(sender, instance=None, created=False, **kwargs):
    if created:
        logger.debug(
            "New user %d triggered a signal to create a default wallet", instance.id
        )
        Wallet.objects.create(user=instance)
