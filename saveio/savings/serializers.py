from rest_framework import serializers

from .models import Stock, Transaction
from .services import StocksMarketService

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
        ticker_info = market_service.get_from_ticker(raw_ticker)
        stock = None

        if ticker_info:
            stock, created = Stock.objects.get_or_create(
                ticker=ticker_info.ticker, defaults={"name": ticker_info.name}
            )

        return stock

    def create(self, validated_data: dict):
        stock = validated_data.pop("ticker")
        validated_data["stock_id"] = stock.id
        return super().create(validated_data)
