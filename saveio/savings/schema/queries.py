import graphene
from graphene_django import DjangoListField, DjangoObjectType
from savings.models import Stock, Transaction


class StockType(DjangoObjectType):
    class Meta:
        model = Stock


class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction


class Query(graphene.ObjectType):
    stocks = DjangoListField(StockType)
    stock_by_id = graphene.Field(StockType, id=graphene.String())

    transactions = DjangoListField(TransactionType)
    transaction_by_id = graphene.Field(TransactionType, id=graphene.String())

    def resolve_stock_by_id(root, info, id):
        return Stock.objects.get(pk=id)

    def resolve_transaction_by_id(root, info, id):
        return Transaction.objects.get(pk=id)
