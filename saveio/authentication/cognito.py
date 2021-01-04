import logging

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication

import requests
from jose import exceptions as jose_exceptions
from jose import jwt

from . import exceptions

logger = logging.getLogger(__name__)


class CognitoAuthentication(BaseAuthentication):
    def __init__(self):
        self.JWKS_URL = settings.COGNITO_JWKS_URL

    @staticmethod
    def _get_exponant_and_modulus(jwk_sets, kid, algorithm):
        for jwk in jwk_sets["keys"]:
            if jwk["kid"] == kid and jwk["alg"] == algorithm:
                return jwk

        raise exceptions.AuthenticationNoRSAException()

    @staticmethod
    def _validate_header_format(header):
        parts = header.split()

        if len(parts) != 2:
            raise exceptions.AuthenticationInvalidHeaderFormatException()

        prefix, token = parts
        if prefix.upper() != "BEARER":
            raise exceptions.AuthenticationInvalidHeaderFormatException()

    def _get_jwks(self, jwks_url=None):
        if not jwks_url:
            jwks_url = self.JWKS_URL

        logger.debug(f"Fetching public keys from {jwks_url}")
        response = requests.get(jwks_url)

        if not response.ok:
            logger.error(f"Invalid public jwks: {jwks_url}")
            raise exceptions.AuthenticationJWTClaimErrorException()
        jwks = response.json()

        return jwks

    def _verify_token(self, jwks, token):
        header = jwt.get_unverified_header(token)
        unverified_body = jwt.get_unverified_claims(token)

        iss = unverified_body["iss"]
        aud = unverified_body["aud"]
        kid = header["kid"]
        algorithm = header["alg"]

        key = self._get_exponant_and_modulus(jwks, kid, algorithm)

        jwt.decode(
            token, key, issuer=iss, audience=aud, options={"verify_at_hash": False}
        )

        return unverified_body

    def _validate_token(self, header):
        _, token = header.split()
        jwks = self._get_jwks()

        try:
            body = self._verify_token(jwks, token)
        except jose_exceptions.ExpiredSignatureError as e:
            raise exceptions.AuthenticationJWTExpiredException() from e
        except jose_exceptions.JWTClaimsError as e:
            raise exceptions.AuthenticationJWTClaimErrorException() from e
        except exceptions.AuthenticationNoRSAException as e:
            raise exceptions.AuthenticationUnableToParseJWTException() from e
        except Exception as e:
            logger.exception(
                "Unknown exception captured during the verify of jwt token"
            )
            raise exceptions.AuthenticationUnableToParseJWTException() from e

        return token, body

    def _handle_user(self, jwt_body):
        """
        Payload example: {
            'sub': 'c6042a21-0227-45aa-aee1-e0f0630a43da',
            'aud': '504u8p26uld4jq484htcu8flov',
            'email_verified': True,
            'event_id': 'e774c736-1e38-4d66-b8d6-175116e43d23',
            'token_use': 'id',
            'auth_time': 1609692024,
            'iss': 'https://cognito-idp.us-east-1.amazonaws.com/[pool_id]',
            'cognito:username': 'guilatrova-local',
            'exp': 1609695624,
            'iat': 1609692024,
            'email': 'email@email.com'
        }
        """

        user, created = User.objects.get_or_create(
            email=jwt_body["email"],
            defaults={
                "username": jwt_body["cognito:username"],
            },
        )

        if created:
            logger.info(f"New user created {user.username} / {user.email}")

        return user

    def process_auth_header(self, auth_header):
        try:
            self._validate_header_format(auth_header)
            token, body = self._validate_token(auth_header)
        except exceptions.AuthenticationException:
            logger.debug(f"AuthenticationException with headers: {auth_header}")
            raise
        except Exception:
            logger.exception("Authorization header raised exception")
            raise
        else:
            user = self._handle_user(body)

        return (user, token)

    def authenticate(self, request):
        """
        https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication
        """
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise exceptions.AuthenticationHeaderNotProvidedException()

        return self.process_auth_header(auth_header)
