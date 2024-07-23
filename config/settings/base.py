from pathlib import Path

from rotary_lights_website.utils import env, load_setting

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / "rotary_lights_website"

READ_DOT_ENV_FILE = load_setting("DJANGO_READ_DOT_ENV_FILE", bool, default=False)
if READ_DOT_ENV_FILE:
    # Caution: OS environment variables take precedence over variables
    env.read_env((BASE_DIR / ".env").as_posix())


# General
# ----------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = load_setting("DJANGO_DEBUG", bool, default=False)

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = load_setting(
    "DJANGO_SECRET_KEY",
    try_env=DEBUG,
)

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS: list[str] = env.list("DJANGO_ALLOWED_HOSTS")

# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with Linux.
TIME_ZONE = "America/Chicago"

# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True


# Databases
# ----------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
# https://docs.djangoproject.com/en/dev/topics/db/transactions/#tying-transactions-to-http-requests
DATABASES = {"default": env.db("DATABASE_URL")}

# Atomic requests are not allowed with async views
DATABASES["default"]["ATOMIC_REQUESTS"] = False

# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# URLs
# ----------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"

# https://docs.djangoproject.com/en/dev/ref/settings/#asgi-application
ASGI_APPLICATION = "config.asgi.application"

# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"


# Security
# ----------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = load_setting(
    "DJANGO_SECURE_SSL_REDIRECT",
    bool,
    default=False,
)

# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True

# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True

# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True

# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True

# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once the former works
SECURE_HSTS_SECONDS = 60

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = load_setting(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
    bool,
    default=True,
)

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = load_setting(
    "DJANGO_SECURE_HSTS_PRELOAD",
    bool,
    default=True,
)

# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = load_setting(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF",
    bool,
    default=True,
)

# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-trusted-origins
CSRF_TRUSTED_ORIGINS = ["https://" + host for host in ALLOWED_HOSTS]

# https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-DATA_UPLOAD_MAX_NUMBER_FIELDS
DATA_UPLOAD_MAX_NUMBER_FIELDS = load_setting(
    "DJANGO_DATA_UPLOAD_MAX_NUMBER_FIELDS",
    int,
    default=None,
)


# Apps
# ----------------------------------------------------------------------
# Standard Django-native apps
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    *(  # Required here, though not directly 1st party django app
        ["daphne"] if DEBUG else []
    ),
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.admin",
    "django.forms",
]

GOOGLE_API_KEY = ""

# Third-party apps
THIRD_PARTY_APPS = [
    "address",
    "allauth_ui",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.mfa",
    "coderedcms",
    "compressor",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_bootstrap5",
    "django_celery_beat",
    "django_sass",
    "polymorphic",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail",
    "wagtail.contrib.settings",
    "wagtail.contrib.table_block",
    "wagtail.admin",
    "wagtailcache",
    "wagtailseo",
    "modelcluster",
    "taggit",
    "phonenumber_field",
    "widget_tweaks",
    "slippers",
    "mjml",
    "birdsong",
    "wagtail_modeladmin",
]

# Local apps
LOCAL_APPS = [
    "rotary_lights_website.contact",
    "rotary_lights_website.content",
    "rotary_lights_website.core",
    "rotary_lights_website.shop",
    "rotary_lights_website.users",
    "rotary_lights_website.volunteering",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# Migrations
# ----------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "rotary_lights_website.contrib.sites.migrations"}


# Authentication
# ----------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"

# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = f"/{load_setting("WAGTAIL_ADMIN_URL", str)}account/"

# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"

# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGOUT_REDIRECT_URL = LOGIN_URL


# Passwords
# ----------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Middleware
# ----------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "wagtailcache.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "wagtailcache.cache.FetchFromCacheMiddleware",
]


# Static
# ----------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(BASE_DIR / "staticfiles")

# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR / "static")]

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


# Media
# ----------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(BASE_DIR / "media")

# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"


# Templates
# ----------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
        "DIRS": [str(APPS_DIR / "templates")],
        # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "rotary_lights_website.users.context_processors.allauth_settings",
            ],
        },
    },
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"


# Fixtures
# ----------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = [str(BASE_DIR / "fixtures")]


# Email
# ----------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = load_setting(
    "DJANGO_EMAIL_BACKEND",
    str,
    default="django.core.mail.backends.smtp.EmailBackend",
)

# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5


# Admin
# ----------------------------------------------------------------------
# Django Admin URL Regex
DJANGO_ADMIN_URL = load_setting("DJANGO_ADMIN_URL", str)
WAGTAIL_ADMIN_URL = load_setting("WAGTAIL_ADMIN_URL", str)

# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ("Dakota Horstman", "dakota.horstman2001@gmail.com"),
]

# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# https://cookiecutter-django.readthedocs.io/en/latest/settings.html#other-environment-settings
# Force the `admin` sign in process to go through the `django-allauth` workflow
DJANGO_ADMIN_FORCE_ALLAUTH = load_setting(
    "DJANGO_ADMIN_FORCE_ALLAUTH",
    bool,
    default=False,
)


# Celery
# ------------------------------------------------------------------------------
if USE_TZ:
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = load_setting("CELERY_BROKER_URL")

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-extended
CELERY_RESULT_EXTENDED = True

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-always-retry
# https://github.com/celery/celery/pull/6122
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-max-retries
CELERY_RESULT_BACKEND_MAX_RETRIES = 10

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 5 * 60

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 60

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-send-task-events
CELERY_WORKER_SEND_TASK_EVENTS = True

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_send_sent_event
CELERY_TASK_SEND_SENT_EVENT = True


# Wagtail
# ----------------------------------------------------------------------
# https://docs.wagtail.org/en/stable/reference/settings.html#wagtail-site-name
WAGTAIL_SITE_NAME = "Rotary Lights of La Crosse"

# https://django-taggit.readthedocs.io/en/latest/getting_started.html
TAGGIT_CASE_INSENSITIVE = True


# wagtail-cache
# ----------------------------------------------------------------------
WAGTAIL_CACHE = load_setting("WAGTAIL_CACHE_ENABLED", bool, default=False)


# django-allauth
# ----------------------------------------------------------------------
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_ADAPTER = "rotary_lights_website.users.adapters.AccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_CHANGE_EMAIL = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_NOTIFICATIONS = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_BLACKLIST = ["admin", "administrator", "root"]
ACCOUNT_ALLOW_REGISTRATION = load_setting(
    "DJANGO_ACCOUNT_ALLOW_REGISTRATION",
    bool,
    default=True,
)

# https://docs.allauth.org/en/latest/account/forms.html
ACCOUNT_FORMS = {"signup": "rotary_lights_website.users.forms.UserSignupForm"}

# https://docs.allauth.org/en/latest/socialaccount/configuration.html
SOCIALACCOUNT_ADAPTER = "rotary_lights_website.users.adapters.SocialAccountAdapter"

# https://docs.allauth.org/en/latest/socialaccount/configuration.html
SOCIALACCOUNT_FORMS = {
    "signup": "rotary_lights_website.users.forms.UserSocialSignupForm",
}

# django-compressor
# ----------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]


# django-phonenumber-field
# ----------------------------------------------------------------------
# https://django-phonenumber-field.readthedocs.io/en/latest/reference.html#phonenumber-default-region
PHONENUMBER_DEFAULT_REGION = "US"


# django-allauth-ui
# ----------------------------------------------------------------------
# https://github.com/danihodovic/django-allauth-ui
ALLAUTH_UI_THEME = "light"


# django-mjml
# ----------------------------------------------------------------------
# https://github.com/liminspace/django-mjml?tab=readme-ov-file#advanced-settings
# Must be False, else raises an ImproperlyConfigured error. Waiting on
# this PR: https://github.com/liminspace/django-mjml/pull/189
MJML_CHECK_CMD_ON_STARTUP = False
