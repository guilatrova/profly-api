from rest_framework import serializers

from markets.services import StocksMarketService

from .models import Stock, Transaction

market_service = StocksMarketService()


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ["stock"]

    ticker = serializers.CharField(write_only=True)

    def validate_ticker(self, raw_ticker):
        stock = market_service.get_stock(raw_ticker)

        if not stock:
            raise serializers.ValidationError(f"{raw_ticker} not found")

        return stock

    def create(self, validated_data: dict):
        stock = validated_data.pop("ticker")
        validated_data["stock_id"] = stock.id
        return super().create(validated_data)