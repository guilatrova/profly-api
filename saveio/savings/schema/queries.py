import graphene
from graphene_django import DjangoListField, DjangoObjectType
from markets.factories import ChartDataFactory
from markets.services import StocksMarketService
from savings.models import Stock, Transaction

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


class StockValueHistory(graphene.ObjectType):
    ticker = graphene.String()
    date = graphene.String()
    open = graphene.String()
    high = graphene.String()
    close = graphene.String()


class Query(graphene.ObjectType):
    # Models
    stocks = DjangoListField(StockType)
    stock_by_id = graphene.Field(StockType, id=graphene.String())

    transactions = DjangoListField(TransactionType)
    transaction_by_id = graphene.Field(TransactionType, id=graphene.String())

    # Adapters
    stock_current_info = graphene.Field(StockInfoType, ticker=graphene.String())

    # Charts
    stocks_units_current_value = graphene.List(StockUnitsCurrentValueType)
    stock_value_history = graphene.List(
        StockValueHistory,
        ticker=graphene.String(),
        period=graphene.String(),
        interval=graphene.String(),
    )

    def resolve_stock_by_id(root, info, id):
        return Stock.objects.get(pk=id)

    def resolve_transaction_by_id(root, info, id):
        return Transaction.objects.get(pk=id)

    def resolve_stock_current_info(root, info, ticker):
        info = market_service.get_stock_info(ticker)
        return info

    def resolve_stocks_units_current_value(root, info):
        return list(data_factory.build_stock_units_current_value())

    def resolve_stock_value_history(root, info, ticker, period, interval):
        return list(data_factory.build_stock_line_factory(ticker, period, interval))
