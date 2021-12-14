import graphene
from graphene_django.rest_framework.mutation import SerializerMutation

from savings.models import SavingTransaction
from savings.serializers import SavingTransactionSerializer


class SavingTransactionMutation(SerializerMutation):
    class Meta:
        serializer_class = SavingTransactionSerializer
        model_operations = ["create"]


class DeleteSavingTransactionMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        SavingTransaction.objects.filter(pk=kwargs["id"]).delete()
        return cls(ok=True)


class Mutation(graphene.ObjectType):
    savingTransactions = SavingTransactionMutation.Field()
    deleteSavingTransaction = DeleteSavingTransactionMutation.Field()
