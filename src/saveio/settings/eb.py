import os

from .debug import *

# DEBUG = False

SECRET_KEY = "!@^(4pb!ft^j2k1)plb=lhfzg(1%307#1@we+#9ae9cqdj2_(^"

# CORS_ORIGIN_ALLOW_ALL = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("RDS_DB_NAME"),
        "USER": os.getenv("RDS_USERNAME"),
        "PASSWORD": os.getenv("RDS_PASSWORD"),
        "HOST": os.getenv("RDS_HOSTNAME"),
        "PORT": os.getenv("RDS_PORT", 5432),
    }
}
