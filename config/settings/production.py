# ruff: noqa: E501
from rotary_lights_website.utils import load_setting

from .base import *  # noqa: F403
from .base import DATABASES, env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["rotarylights.org"])

# DATABASES
# ------------------------------------------------------------------------------
DATABASES["default"]["CONN_MAX_AGE"] = load_setting("CONN_MAX_AGE", int, default=60)

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": load_setting("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # Mimicing memcache behavior.
            # https://github.com/jazzband/django-redis#memcached-exceptions-behavior
            "IGNORE_EXCEPTIONS": True,
        },
    },
}


# Wagtail
# ----------------------------------------------------------------------
# https://docs.wagtail.org/en/stable/reference/settings.html#wagtailadmin-base-url
WAGTAILADMIN_BASE_URL = load_setting("WAGTAILADMIN_BASE_URL")

# # STORAGES
# # ------------------------------------------------------------------------------
# # https://django-storages.readthedocs.io/en/latest/#installation
# INSTALLED_APPS += ["storages"]
# # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
# AWS_ACCESS_KEY_ID = env("DJANGO_AWS_ACCESS_KEY_ID")
# # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
# AWS_SECRET_ACCESS_KEY = env("DJANGO_AWS_SECRET_ACCESS_KEY")
# # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
# AWS_STORAGE_BUCKET_NAME = env("DJANGO_AWS_STORAGE_BUCKET_NAME")
# # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
# AWS_QUERYSTRING_AUTH = False
# # DO NOT change these unless you know what you're doing.
# _AWS_EXPIRY = 60 * 60 * 24 * 7
# # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
# AWS_S3_OBJECT_PARAMETERS = {
#     "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate",
# }
# # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
# AWS_S3_MAX_MEMORY_SIZE = env.int(
#     "DJANGO_AWS_S3_MAX_MEMORY_SIZE",
#     default=100_000_000,  # 100MB
# )
# # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
# AWS_S3_REGION_NAME = env("DJANGO_AWS_S3_REGION_NAME", default=None)
# # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#cloudfront
# AWS_S3_CUSTOM_DOMAIN = env("DJANGO_AWS_S3_CUSTOM_DOMAIN", default=None)
# aws_s3_domain = AWS_S3_CUSTOM_DOMAIN or f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
# # STATIC & MEDIA
# # ------------------------
# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.s3.S3Storage",
#         "OPTIONS": {
#             "location": "media",
#             "file_overwrite": False,
#         },
#     },
#     "staticfiles": {
#         "BACKEND": "storages.backends.s3.S3Storage",
#         "OPTIONS": {
#             "location": "static",
#             "default_acl": "public-read",
#         },
#     },
# }
# MEDIA_URL = f"https://{aws_s3_domain}/media/"
# COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"
# STATIC_URL = f"https://{aws_s3_domain}/static/"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = load_setting(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="Rotary Lights Website <noreply@rotarylights.org>",
)

# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = load_setting("DJANGO_EMAIL_HOST")

# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = load_setting("DJANGO_EMAIL_PORT")

# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST_PASSWORD = load_setting(
    "DJANGO_EMAIL_HOST_PASSWORD", try_env=True
)  # TODO: False

# https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = load_setting("DJANGO_EMAIL_HOST_USER")

# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = load_setting(
    "DJANGO_EMAIL_SUBJECT_PREFIX",
    default="[Rotary Lights] ",
)

# https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = load_setting("DJANGO_EMAIL_USE_TLS", default=True)

# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = load_setting("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)


# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = load_setting("DJANGO_ADMIN_URL")

# Anymail
# ------------------------------------------------------------------------------
# https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
# INSTALLED_APPS += ["anymail"]
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference
# https://anymail.readthedocs.io/en/stable/esps/mailgun/
# EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
# ANYMAIL = {
#     "MAILGUN_API_KEY": env("MAILGUN_API_KEY"),
#     "MAILGUN_SENDER_DOMAIN": env("MAILGUN_DOMAIN"),
#     "MAILGUN_API_URL": env("MAILGUN_API_URL", default="https://api.mailgun.net/v3"),
# }

# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_ENABLED
# COMPRESS_ENABLED = env.bool("COMPRESS_ENABLED", default=True)
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_STORAGE
# COMPRESS_STORAGE = STORAGES["staticfiles"]["BACKEND"]
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_URL
# COMPRESS_URL = STATIC_URL
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_FILTERS
# COMPRESS_FILTERS = {
#     "css": [
#         "compressor.filters.css_default.CssAbsoluteFilter",
#         "compressor.filters.cssmin.rCSSMinFilter",
#     ],
#     "js": ["compressor.filters.jsmin.JSMinFilter"],
# }
# Collectfast
# ------------------------------------------------------------------------------
# https://github.com/antonagestam/collectfast#installation
# INSTALLED_APPS = ["collectfast", *INSTALLED_APPS]

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console", "mail_admins"],
            "propagate": True,
        },
    },
}
