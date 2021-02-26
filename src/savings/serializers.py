import logging

from rest_framework import serializers

from markets.services import StocksMarketService

from .models import Stock, Transaction

market_service = StocksMarketService()
logger = logging.getLogger(__name__)


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ["stock"]
        read_only_fields = ["user"]

    ticker = serializers.CharField(write_only=True)

    def validate_ticker(self, raw_ticker):
        print("* Validating ticker")
        print(f"Validating ticker {raw_ticker}")
        stock = market_service.get_stock(raw_ticker)
        print(f"Got stock data: {stock}")

        if not stock:
            raise serializers.ValidationError(f"{raw_ticker} not found")

        return stock

    def create(self, validated_data: dict):
        print(f"Creating transaction with initial data {validated_data}")
        user = self.context["request"].user
        stock = validated_data.pop("ticker")

        validated_data["stock_id"] = stock.id
        validated_data["user"] = user

        print(f"Augmenting data: {validated_data}")
        instance = super().create(validated_data)
        print(f"Instance: {instance}")
        return instance
