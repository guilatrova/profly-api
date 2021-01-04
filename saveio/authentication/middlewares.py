# https://github.com/graphql-python/graphene-django/issues/345#issuecomment-616896108
from authentication import CognitoAuthentication


class BearerTokenAuthMiddleware:
    def __init__(self):
        self.auth = CognitoAuthentication()

    def resolve(self, next, root, info, **args):
        auth_header = info.context.META.get("HTTP_AUTHORIZATION")

        if auth_header:
            user, token = self.auth.process_auth_header(auth_header)
            info.context.user = user

        return next(root, info, **args)
