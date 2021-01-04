# from django.contrib.auth.mixins import LoginRequiredMixin

from graphene_django.views import GraphQLView


class PrivateGraphQLView(GraphQLView):
    pass
