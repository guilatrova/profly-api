import graphene
from graphene_django import DjangoListField, DjangoObjectType
from savings.models import Stock, Transaction
from savings.services import ChartDataFactory, StocksMarketService

market_service = StocksMarketService()
data_factory = ChartDataFactory()


class StockType(DjangoObjectType):
    class Meta:
        model = Stock


class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction

    value = graphene.Float()

    def resolve_value(self, info):
        return self.value


class StockInfoType(graphene.ObjectType):
    """Gathers stock with price at the moment"""

    name = graphene.String()
    ticker = graphene.String()
    currency = graphene.String()
    current_price = graphene.Float()
    logo_url = graphene.String()
    timestamp = graphene.DateTime()


class StockUnitsCurrentValueType(graphene.ObjectType):
    ticker = graphene.String()
    total_units = graphene.Float()
    close_price = graphene.Float()
    total_value = graphene.Float()


class Query(graphene.ObjectType):
    stocks = DjangoListField(StockType)
    stock_by_id = graphene.Field(StockType, id=graphene.String())
    stock_current_info = graphene.Field(StockInfoType, ticker=graphene.String())

    transactions = DjangoListField(TransactionType)
    transaction_by_id = graphene.Field(TransactionType, id=graphene.String())

    stocks_units_current_value = graphene.List(StockUnitsCurrentValueType)

    def resolve_stock_by_id(root, info, id):
        return Stock.objects.get(pk=id)

    def resolve_transaction_by_id(root, info, id):
        return Transaction.objects.get(pk=id)

    def resolve_stock_current_info(root, info, ticker):
        info = market_service.get_from_ticker(ticker)
        return info

    def resolve_stocks_units_current_value(root, info):
        return list(data_factory.build_stock_units_current_value())
