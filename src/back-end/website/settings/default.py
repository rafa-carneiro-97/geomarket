import os
from pathlib import Path
from email.utils import getaddresses
from django.urls import reverse_lazy
from dotenv import load_dotenv
from .logging import *


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Get environment variables from .env file
load_dotenv(dotenv_path=BASE_DIR / ".env")

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]

DEBUG = True

ALLOWED_HOSTS = os.environ["DJANGO_ALLOWED_HOSTS"].split(",")
CSRF_TRUSTED_ORIGINS = os.environ["DJANGO_CSRF_TRUSTED_ORIGINS"].split(",")


# Application definition

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "channels",
    # APPS
    "apps.core",
    "apps.users",
    "apps.business",
    "apps.sales",
    "apps.api",
    "apps.spa",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "website.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


ASGI_APPLICATION = "website.asgi.application"


# Websocket
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.User"


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Fortaleza"

USE_I18N = True

USE_TZ = True


LANGUAGES = [
    ("pt-br", "Brazilian Portuguese"),
]


# URL for tatic files (CSS, JavaScript, Images)
STATIC_URL = "static/"
# The absolute path to the directory where collectstatic will collect static files for deployment
STATIC_ROOT = BASE_DIR / "staticfiles"


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Media
# URL to use when referring to media files
MEDIA_URL = "/media/"
# The absolute path to the media directory
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# URLS
LOGIN_URL = "/login"
LOGOUT_REDIRECT_URL = "/sair"

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    },
}

# Session
SESSION_COOKIE_AGE = 3600 * 24 * 14  # 14 days
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"  # Caches default

# Email
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = os.environ["EMAIL_PORT"]
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
DEFAULT_FROM_EMAIL = "Geomarket <%s>" % os.environ["EMAIL_HOST_USER"]
EMAIL_SUPPORT = os.environ["EMAIL_SUPPORT"]


SERVER_EMAIL = DEFAULT_FROM_EMAIL
# A list of all the administrators who get code error notifications.
ADMINS = getaddresses([os.environ.get("DJANGO_ADMINS", default=None)])
