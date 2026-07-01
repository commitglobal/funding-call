"""
Specific settings for the automated test environment
"""

import os

from .settings import *  # noqa: F405, F403, F401
from .settings import BASE_DIR

DJANGO_VITE["default"]["dev_mode"] = True
DJANGO_VITE["default"]["dev_server_port"] = 3000


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.abspath(os.path.join(BASE_DIR, ".db_sqlite", "test.sqlite3")),
    }
}

if env("DATABASE_ENGINE") == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": env("DATABASE_NAME"),
            "USER": "root",
            "PASSWORD": env("DATABASE_PASSWORD"),
            "HOST": env("DATABASE_HOST"),
            "PORT": env("DATABASE_PORT"),
        }
    }

SECRET_KEY = "test"
