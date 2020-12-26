import graphene
from graphene_django import DjangoListField, DjangoObjectType
from graphene_django.rest_framework.mutation import SerializerMutation

from .models import Stock, Transaction
from .serializers import StockSerializer, TransactionSerializer


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


class StockMutation(SerializerMutation):
    class Meta:
        serializer_class = StockSerializer
        model_operations = ["create"]


class TransactionMutation(SerializerMutation):
    class Meta:
        serializer_class = TransactionSerializer
        model_operations = ["create"]


class Mutation(graphene.ObjectType):
    stocks = StockMutation.Field()
    transactions = TransactionMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
