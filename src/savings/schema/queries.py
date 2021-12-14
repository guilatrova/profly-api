import graphene
from graphene_django import DjangoListField

from savings.models import Wallet

from . import types


class ModelQuery(graphene.ObjectType):
    wallet = graphene.Field(types.WalletType)
    saving_transactions = DjangoListField(types.SavingTransactionType)

    def resolve_wallet(root, info, id):
        if info.context.user.is_anonymous:
            return None

        return Wallet.objects.get_default_wallet(info.context.user)


class Query(ModelQuery, graphene.ObjectType):
    pass
