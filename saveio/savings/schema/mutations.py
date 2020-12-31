import graphene
from graphene_django.rest_framework.mutation import SerializerMutation
from savings.models import Transaction
from savings.serializers import StockSerializer, TransactionSerializer


class StockMutation(SerializerMutation):
    class Meta:
        serializer_class = StockSerializer
        model_operations = ["create"]


class TransactionMutation(SerializerMutation):
    class Meta:
        serializer_class = TransactionSerializer
        model_operations = ["create"]


class DeleteTransactionMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        Transaction.objects.filter(pk=kwargs["id"]).delete()
        return cls(ok=True)


class Mutation(graphene.ObjectType):
    stocks = StockMutation.Field()
    transactions = TransactionMutation.Field()
    deleteTransaction = DeleteTransactionMutation.Field()
