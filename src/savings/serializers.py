import logging

from rest_framework import serializers

from .models import SavingTransaction, Wallet

logger = logging.getLogger(__name__)


class SavingTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingTransaction
        exclude = ["wallet"]
        read_only_fields = ["created_at"]

    def create(self, validated_data: dict):
        user = self.context["request"].user
        from django.contrib.auth.models import User

        user = User.objects.first()
        validated_data["wallet"] = Wallet.objects.get_default_wallet(user)

        logger.info(f"Creating saving transaction with data: {validated_data}")
        return super().create(validated_data)
