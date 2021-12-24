import os

from .base import *

DEBUG = False
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")  # type: ignore

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USERNAME"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOSTNAME"),
        "PORT": os.getenv("DB_PORT", 5432),
    }
}

# NETWORK & CORS
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost,*").split(",")

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    "https://www.profly.app",
    "https://profly.app",
)
