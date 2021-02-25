import os

from django.core.management.utils import get_random_secret_key

from .debug import *

# STATIC FILES
STATIC_ROOT = BASE_DIR / "staticfiles"

# BASE
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())
DEBUG = os.getenv("DEBUG", "False") == "True"

# NETWORK
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost,*").split(",")
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    "profly-i7f6f.ondigitalocean.app",
    "https://www.profly.app",
)
