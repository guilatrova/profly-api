from rest_framework import exceptions, status


class AuthenticationException(exceptions.APIException):
    """The only purpose of this exception is to allow
    identifying and catching any Authentication exceptions
    """

    detail = None
    status_code = None

    def __init__(self, detail, status_code=status.HTTP_403_FORBIDDEN):
        self.detail = detail
        self.status_code = status_code


class AuthenticationHeaderNotProvidedException(AuthenticationException):
    """Exception raised whenever the authentication header is not provided."""

    def __init__(self):
        detail = "Authentication credentials were not provided."
        super().__init__(detail)


class AuthenticationLoginFailedException(AuthenticationException):
    """Exception raised whenever the login fail because of the credentials."""

    def __init__(self):
        detail = "Invalid credentials."
        super().__init__(detail)


class AuthenticationInvalidHeaderFormatException(AuthenticationException):
    """Exception raised whenever the authentication header is not the correct
    format (Bearer).
    """

    def __init__(self):
        detail = "Authorization header must be Bearer token."
        super().__init__(detail)


class AuthenticationNoRSAException(AuthenticationException):
    """Exception raised whenever the rsa is not found."""

    def __init__(self):
        detail = "Unable to find appropriate key."
        super().__init__(detail)


class AuthenticationJWTExpiredException(AuthenticationException):
    """Exception raised whenever the JWT is expired."""

    def __init__(self):
        detail = "Token expired."
        super().__init__(detail)


class AuthenticationJWTClaimErrorException(AuthenticationException):
    """Exception raised whenever the JWT claim raises a error."""

    def __init__(self):
        detail = "JWT Claim Error."
        super().__init__(detail)


class AuthenticationUnableToParseJWTException(AuthenticationException):
    """Exception raised whenever is not possible to parse JWT."""

    def __init__(self):
        detail = "Unable to parse token."
        super().__init__(detail)
