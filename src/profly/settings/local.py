import os

from .base import *

SECRET_KEY = "!@^(4pb!ft^j2k1)plb=lhfzg(1%307#1@we+#9ae9cqdj2_(^"
CORS_ORIGIN_ALLOW_ALL = True

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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"rich": {"datefmt": "[%X]"}},
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "formatter": "rich",
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
}
