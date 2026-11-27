"""Supported Django settings for the Gymkhana Stampede application."""
import os

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in ("1", "true", "yes", "on"):
        return True
    if normalized in ("0", "false", "no", "off"):
        return False
    raise ImproperlyConfigured(
        f"{name} must be an explicit boolean value (true/false, yes/no, on/off, or 1/0)."
    )


SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY or not SECRET_KEY.strip():
    raise ImproperlyConfigured("Set DJANGO_SECRET_KEY before starting Gymkhana Stampede.")
if len(SECRET_KEY) < 50 or len(set(SECRET_KEY)) < 5:
    raise ImproperlyConfigured(
        "DJANGO_SECRET_KEY must be at least 50 characters and contain at least 5 distinct characters."
    )

DEBUG = env_bool("DJANGO_DEBUG", False)
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "Derby_Event.apps.DerbyEventConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "KDF.urls"
WSGI_APPLICATION = "KDF.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Login works for provisioned accounts. Public signup stays disabled until
# Participant-profile onboarding and verified email delivery are implemented.
ACCOUNT_LOGIN_METHODS = {"username", "email"}
ACCOUNT_SIGNUP_FIELDS = ["username*", "email*", "password1*", "password2*"]
ACCOUNT_SIGNUP_ENABLED = False
ACCOUNT_UNIQUE_EMAIL = True
LOGIN_REDIRECT_URL = "/Derby_Event/landing_page/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/Derby_Event/"

DB_ENGINE = os.environ.get("DJANGO_DB_ENGINE", "sqlite").strip().lower()
if DB_ENGINE in ("postgres", "postgresql"):
    required_db_values = ("DJANGO_DB_NAME", "DJANGO_DB_USER", "DJANGO_DB_PASSWORD", "DJANGO_DB_HOST")
    missing_db_values = [name for name in required_db_values if not os.environ.get(name)]
    if missing_db_values:
        raise ImproperlyConfigured(
            "PostgreSQL requires these environment variables: " + ", ".join(missing_db_values)
        )
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["DJANGO_DB_NAME"],
            "USER": os.environ["DJANGO_DB_USER"],
            "PASSWORD": os.environ["DJANGO_DB_PASSWORD"],
            "HOST": os.environ["DJANGO_DB_HOST"],
            "PORT": os.environ.get("DJANGO_DB_PORT", "5432"),
            "CONN_MAX_AGE": int(os.environ.get("DJANGO_DB_CONN_MAX_AGE", "60")),
        }
    }
elif DB_ENGINE == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.environ.get("DJANGO_DATABASE_NAME") or os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    raise ImproperlyConfigured("DJANGO_DB_ENGINE must be sqlite or postgresql.")

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Kentucky/Louisville"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.environ.get("DJANGO_MEDIA_ROOT", os.path.join(BASE_DIR, "media"))

DEFAULT_FROM_EMAIL = os.environ.get("DJANGO_DEFAULT_FROM_EMAIL", "webmaster@localhost")
EMAIL_BACKEND = os.environ.get(
    "DJANGO_EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)

# Optional keys are read only from the hosting environment.
GOOGLE_MAPS_BROWSER_API_KEY = os.environ.get("GOOGLE_MAPS_BROWSER_API_KEY", "")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", not DEBUG)
SESSION_COOKIE_SECURE = env_bool("DJANGO_SESSION_COOKIE_SECURE", not DEBUG)
CSRF_COOKIE_SECURE = env_bool("DJANGO_CSRF_COOKIE_SECURE", not DEBUG)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("DJANGO_HSTS_INCLUDE_SUBDOMAINS", False)
SECURE_HSTS_PRELOAD = env_bool("DJANGO_HSTS_PRELOAD", False)

if env_bool("DJANGO_TRUST_PROXY", False):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
