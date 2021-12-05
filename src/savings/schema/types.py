import graphene
from graphene_django import DjangoObjectType

from savings.models import Stock, Transaction

from .connections import CustomConnection


class StockType(DjangoObjectType):
    class Meta:
        model = Stock

    id = graphene.ID(source="pk", required=True)


class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction
        filter_fields = {
            "stock__ticker": ["exact"],
            "performed_at": ["exact", "lte", "gte"],
        }
        interfaces = (graphene.Node,)
        connection_class = CustomConnection

    id = graphene.ID(source="pk", required=True)
    value = graphene.Float()

    @classmethod
    def get_queryset(cls, queryset, info):
        if info.context.user.is_anonymous:
            return queryset.none()

        return queryset.filter(user=info.context.user)

    def resolve_value(self, info):
        return self.value


class CurrencyRate(graphene.ObjectType):
    """Gathers rate between 2 currencies at the moment"""

    from_currency = graphene.String()
    to_currency = graphene.String()
    rate = graphene.Float()


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
    name = graphene.String()
    logo_url = graphene.String()
    currency = graphene.String()
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
    currency = graphene.String()


class OwnedStockSummary(graphene.ObjectType):
    ticker = graphene.String()
    currency = graphene.String()
    units = graphene.Float()
    average_buy_price = graphene.Float()
    average_sell_price = graphene.Float()
    current_value = graphene.Float()
