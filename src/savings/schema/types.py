import graphene
from graphene_django import DjangoObjectType

from profly.graphene_connections import CustomConnection
from savings.models import SavingTransaction, Wallet


class WalletType(DjangoObjectType):
    class Meta:
        model = Wallet

    id = graphene.ID(source="pk", required=True)
    value = graphene.Float()

    @classmethod
    def get_queryset(cls, queryset, info):
        if info.context.user.is_anonymous:
            return queryset.none()

        return queryset.filter(user=info.context.user)

    def resolve_value(self, info):
        return SavingTransaction.objects.aggregate_wallet_current_value(wallet=self)


class SavingTransactionType(DjangoObjectType):
    class Meta:
        model = SavingTransaction
        filter_fields = {
            "wallet__name": ["exact"],
            "performed_at": ["exact", "lte", "gte"],
        }
        interfaces = (graphene.Node,)
        connection_class = CustomConnection

    id = graphene.ID(source="pk", required=True)

    @classmethod
    def get_queryset(cls, queryset, info):
        if info.context.user.is_anonymous:
            return queryset.none()

        return queryset.filter(wallet__user=info.context.user)
