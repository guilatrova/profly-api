import json
import os

from django.http import HttpResponse
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated

from authentication import CognitoAuthentication
from authentication.exceptions import AuthenticationException
from graphene_django.views import GraphQLView


def index(request):
    version = os.getenv("COMMIT_HASH")
    return HttpResponse(f"profly-api@{version}")


class PrivateGraphQLView(GraphQLView):
    authentication_classes = [CognitoAuthentication]
    permission_classes = [IsAuthenticated]

    def authenticate_request(self, request):
        for auth_class in self.authentication_classes:
            auth_tuple = auth_class().authenticate(request)
            if auth_tuple:
                request.user, request.token = auth_tuple
                break

    def check_permissions(self, request):
        for permission_class in self.permission_classes:
            if not permission_class().has_permission(request, self):
                return False
        return True

    def dispatch(self, request, *args, **kwargs):
        try:
            self.authenticate_request(request)
            has_permission = self.check_permissions(request)
            if not has_permission:
                return HttpResponse(
                    json.dumps({"errors": ["permission denied"]}),
                    status=status.HTTP_403_FORBIDDEN,
                    content_type="application/json",
                )
        except (AuthenticationFailed, AuthenticationException) as err:
            return HttpResponse(
                json.dumps({"errors": [str(err)]}),
                status=status.HTTP_401_UNAUTHORIZED,
                content_type="application/json",
            )

        return super().dispatch(request, *args, **kwargs)
