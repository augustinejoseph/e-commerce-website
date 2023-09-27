from pathlib import Path
import os
import environ

env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = env("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "False") == "True"
print("Debug", DEBUG)
ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "chartjs",
    "crispy_forms",
    "adminPanel",
    "wishlist",
    "orders",
    "django_filters",
    "cart",
    "dashboard",
    "category",
    "pages",
    "products",
    "accounts",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]
CRISPY_TEMPLATE_PACK = "bootstrap4"
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ecommerce.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "adminPanel/templates",
            "templates",
            "customAdmin/templates",
            "ecommerce/templates",
            "accounts/templates",
            "pages/templates",
            "dashboard/templates",
            "cart/templates",
            "orders/templates",
            "wishlist/templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "category.contextProcessor.menuList",
                # 'cart.contextProcessor.counter',
                "adminPanel.contextProcessor.countData",
            ],
        },
    },
]

WSGI_APPLICATION = "ecommerce.wsgi.application"

AUTH_USER_MODEL = "accounts.Account"

if DEBUG == True:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST"),
            "PORT": env("DB_PORT"),
        }
    }


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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


if DEBUG == True:
    STATIC_URL = "/static/"
    STATIC_ROOT = BASE_DIR / "static"
    STATICFILES_DIRS = [
        "adminPanel/static/",
        "ecommerce/static/",
        "accounts/static",
        "pages/static",
        "dashboard/static",
        "cart/static/",
        "wishlist/static",
    ]
else:
    STATIC_URL = "/static/"
    import os

    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "adminPanel", "static"),
        os.path.join(BASE_DIR, "ecommerce", "static"),
        os.path.join(BASE_DIR, "accounts", "static"),
        os.path.join(BASE_DIR, "pages", "static"),
        os.path.join(BASE_DIR, "dashboard", "static"),
        os.path.join(BASE_DIR, "cart", "static"),
        os.path.join(BASE_DIR, "wishlist", "static"),
    ]


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# danger : bootstrap danger
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: "danger",
}


# SMTP Configuration
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = 587
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True


# media files configuration
if DEBUG == True:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media/"
else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = "/home/developer_augustine/happyfeets/media"
    # BASE_DIR/'media/'


RAZOR_KEY_ID = env("RAZOR_KEY_ID")
RAZOR_KEY_SECRET = env("RAZOR_KEY_SECRET")


ADMINS = [
    ("Augustine", env("EMAIL_HOST_USER")),
]
