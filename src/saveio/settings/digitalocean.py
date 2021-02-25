import os

from django.core.management.utils import get_random_secret_key

from .debug import *

STATIC_ROOT = BASE_DIR / "staticfiles"

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost,*").split(",")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())
