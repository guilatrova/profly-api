import graphene
from graphene_django import DjangoObjectType
from savings.models import Stock, Transaction


class ExtendedConnection(graphene.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()
    edge_count = graphene.Int()

    def resolve_total_count(root, info, **kwargs):
        return root.length

    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)


class StockType(DjangoObjectType):
    class Meta:
        model = Stock


class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction
        filter_fields = ["stock__ticker", "performed_at"]
        interfaces = (graphene.Node,)
        connection_class = ExtendedConnection

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
    date = graphene.Date()
    open = graphene.Float()
    high = graphene.Float()
    close = graphene.Float()


class StockTransactionsValueHistory(graphene.ObjectType):
    history = graphene.List(StockValueHistory)
    transactions = graphene.List(TransactionType)


class OwnedStockSummary(graphene.ObjectType):
    ticker = graphene.String()
    units = graphene.Float()
    average_buy_price = graphene.Float()
    average_sell_price = graphene.Float()
