import graphene
from graphene_django.rest_framework.mutation import SerializerMutation
from savings.serializers import StockSerializer, TransactionSerializer


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
