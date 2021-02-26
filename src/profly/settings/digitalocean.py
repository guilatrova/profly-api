import os
import sys

from django.core.management.utils import get_random_secret_key

import dj_database_url

from .debug import *

# STATIC FILES
STATIC_ROOT = BASE_DIR / "staticfiles"

# BASE
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())
DEBUG = os.getenv("DEBUG", "False") == "True"

# DATABASE
if len(sys.argv) > 1 and sys.argv[1] != "collectstatic":
    db_url = os.getenv("DATABASE_URL", None)
    if db_url is None:
        raise Exception("DATABASE_URL environment variable not defined")

    DATABASES = {
        "default": dj_database_url.parse(db_url),
    }

# NETWORK
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost,*").split(",")
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    "https://profly-i7f6f.ondigitalocean.app",
    "https://www.profly.app",
    "https://web.profly.app",
)
