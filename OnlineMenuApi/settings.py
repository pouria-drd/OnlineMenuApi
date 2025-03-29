import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: Keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: Don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

AUTH_USER_MODEL = "users.UserModel"

# ---------------------------------------------------------------
# Application definition
# ---------------------------------------------------------------

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",  # Django admin interface
    "django.contrib.auth",  # User authentication
    "django.contrib.contenttypes",  # Content type framework
    "django.contrib.sessions",  # Session management
    "django.contrib.messages",  # Message framework
    "django.contrib.staticfiles",  # Static file management
    # Third-party apps
    "corsheaders",  # Cross-origin resource sharing
    "rest_framework",  # Django REST framework for building APIs
    "django_filters",  # Filtering for Django REST framework
    "rest_framework_simplejwt",  # JSON Web Token authentication
    "django_cleanup.apps.CleanupSelectedConfig",  # Clean up unused media files
    # Custom apps
    "users",
]

# Middleware configuration
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Security middleware
    "django.contrib.sessions.middleware.SessionMiddleware",  # Session middleware
    "django.middleware.common.CommonMiddleware",  # Common middleware
    "django.middleware.csrf.CsrfViewMiddleware",  # CSRF protection
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Authentication middleware
    "django.contrib.messages.middleware.MessageMiddleware",  # Message middleware
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Prevent clickjacking
]

# Debug Toolbar (optional)
ENABLE_DEBUG_TOOLBAR = os.getenv("ENABLE_DEBUG_TOOLBAR", "False").lower() == "true"
if ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS.append("debug_toolbar")  # Add debug toolbar to apps
    MIDDLEWARE.insert(
        0, "debug_toolbar.middleware.DebugToolbarMiddleware"
    )  # Add debug toolbar to middleware

# Root URL configuration
ROOT_URLCONF = "OnlineMenuApi.urls"

# Template settings (if using Django templates)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # Specify template directories here if using them
        "APP_DIRS": True,  # Automatically find templates in app directories
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",  # Debug information
                "django.template.context_processors.request",  # Request context
                "django.contrib.auth.context_processors.auth",  # User authentication context
                "django.contrib.messages.context_processors.messages",  # Messages context
            ],
        },
    },
]

# WSGI application configuration
WSGI_APPLICATION = "OnlineMenuApi.wsgi.application"

# ---------------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------------

# SQLite Database (for development)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "OnlineMenuApiDataBase.sqlite3",  # SQLite DB file location
    }
}

# Uncomment and configure if using PostgreSQL
# DATABASES = {
#     "default": {
#         "HOST": os.environ.get("DB_HOST", ""),
#         "PORT": os.environ.get("DB_PORT", ""),
#         "ENGINE": os.environ.get("DB_ENGINE", ""),
#         "NAME": os.environ.get("POSTGRES_DB", ""),
#         "USER": os.environ.get("POSTGRES_USER", ""),
#         "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
#     }
# }

# ---------------------------------------------------------------
# Authentication Backends
# ---------------------------------------------------------------

AUTHENTICATION_BACKENDS = [
    "users.backends.AuthBackend",  # Custom authentication backend
    "django.contrib.auth.backends.ModelBackend",  # Default Django authentication
]

# ---------------------------------------------------------------
# Password Validation
# ---------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------
# Localization and Time Zones
# ---------------------------------------------------------------

LANGUAGE_CODE = "en-us"  # Default language

# Time zone setup from environment variable (default to UTC)
TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
USE_TZ = os.getenv("USE_TZ", "False") == "True"  # Whether to use time zones
USE_I18N = os.getenv("USE_I18N", "False") == "True"  # Internationalization setting

# ---------------------------------------------------------------
# Static and Media Files Configuration
# ---------------------------------------------------------------

# Static files URL and root directory
STATIC_URL = os.getenv("STATIC_URL", "static/")  # Default is "static/"
STATIC_ROOT = os.path.join(BASE_DIR, os.getenv("STATIC_ROOT", "static"))

# Media files URL and root directory
MEDIA_URL = os.getenv("MEDIA_URL", "/media/")  # Default is "/media/"
MEDIA_ROOT = BASE_DIR / os.getenv("MEDIA_ROOT", "media")

# ---------------------------------------------------------------
# Default Primary Key Field Type
# ---------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------
# Allowed Hosts Configuration
# ---------------------------------------------------------------

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(
    ","
)  # Allowed hosts from environment variable
INTERNAL_IPS = os.getenv("INTERNAL_IPS", "127.0.0.1").split(
    ","
)  # Internal IPs for debug toolbar

# ---------------------------------------------------------------
# CORS Configuration
# ---------------------------------------------------------------

CORS_ALLOW_CREDENTIALS = (
    os.getenv("CORS_ALLOW_CREDENTIALS", "False") == "True"
)  # Whether to allow credentials in CORS
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(
    ","
)  # List of allowed origins for CORS
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]  # Allowed HTTP methods for CORS

# ---------------------------------------------------------------
# Django REST Framework Configuration
# ---------------------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        # "rest_framework.permissions.IsAuthenticated",  # Only authenticated users can access
        "rest_framework.permissions.AllowAny",  #  Allow anonymous users to access
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # JWT authentication
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",  # Throttle based on user rate
        "rest_framework.throttling.AnonRateThrottle",  # Throttle based on anonymous user rate
        "rest_framework.throttling.ScopedRateThrottle",  # Throttle based on scope
    ],
    "DEFAULT_THROTTLE_RATES": {
        "user": os.getenv("USER_THROTTLE_RATE", "20/minute"),
        "anon": os.getenv("ANON_THROTTLE_RATE", "10/minute"),
    },
}

# ---------------------------------------------------------------
# Simple JWT Configuration
# ---------------------------------------------------------------

minutes = int(os.environ.get("ACCESS_TOKEN_LIFETIME", 15))
hours = int(os.environ.get("REFRESH_TOKEN_LIFETIME", 24))

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=minutes),  # Access token lifetime
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=hours),  # Refresh token lifetime
    "AUTH_HEADER_TYPES": ("Bearer",),  # Authentication header type
    "UPDATE_LAST_LOGIN": True,  # Update last login time when refreshing token
}

# ---------------------------------------------------------------
# Email Configuration
# ---------------------------------------------------------------

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)  # Email backend
EMAIL_HOST = os.getenv("EMAIL_HOST")  # SMTP host
EMAIL_PORT = os.getenv("EMAIL_PORT", 587)  # SMTP port
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")  # SMTP user
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")  # Default email sender
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  # SMTP password
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False") == "True"  # Use TLS encryption

# ---------------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # Keep existing loggers active
    "handlers": {
        "login_file_v1": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.getenv(
                "LOGIN_LOG_FILE", "login_activity_v1.log"
            ),  # Login activity log file
        },
        "login_console_v1": {
            "level": "INFO",
            "class": "logging.StreamHandler",  # Log to console
        },
        "email_file_v1": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.getenv(
                "EMAIL_LOG_FILE", "email_activity_v1.log"
            ),  # Email activity log file
        },
        "email_console_v1": {
            "level": "INFO",
            "class": "logging.StreamHandler",  # Log to console
        },
    },
    "loggers": {
        "login_v1": {
            "handlers": ["login_file_v1", "login_console_v1"],
            "level": "INFO",
            "propagate": True,
        },
        "email_v1": {
            "handlers": ["email_file_v1", "email_console_v1"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
