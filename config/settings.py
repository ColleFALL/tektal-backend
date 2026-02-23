
# from datetime import timedelta
# import os
# from pathlib import Path

# import dj_database_url
# from dotenv import load_dotenv
# import cloudinary


# load_dotenv()

# BASE_DIR = Path(__file__).resolve().parent.parent

# # =========================
# # SECURITY
# # =========================
# SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")
# DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

# ALLOWED_HOSTS = os.environ.get(
#     "DJANGO_ALLOWED_HOSTS",
#     "127.0.0.1,localhost"
# ).split(",")
# # =========================
# # APPS
# # =========================
# INSTALLED_APPS = [
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",

#     # Cloudinary (ordre important)
#     "cloudinary_storage",
#     "django.contrib.staticfiles",
#     "cloudinary",

#     # Third-party
#     "rest_framework",
#     "rest_framework_simplejwt",
#     "rest_framework_simplejwt.token_blacklist",
#     "djoser",
#     "corsheaders",

#     # Local apps
#     "accounts",
#     "core",
#     "paths",
#     "admin_panel",
# ]


# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.SessionAuthentication',
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#     ],
# }

# # ========================
# # MIDDLEWARE
# # =========================
# MIDDLEWARE = [
#     "corsheaders.middleware.CorsMiddleware",
#     "django.middleware.security.SecurityMiddleware",
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]

# ROOT_URLCONF = "config.urls"
# WSGI_APPLICATION = "config.wsgi.application"
# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": [BASE_DIR / "templates"],  # optionnel mais recommandé
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.debug",
#                 "django.template.context_processors.request",
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#             ],
#         },
#     },
# ]


# # =========================
# # DATABASE
# # =========================
# DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

# if DATABASE_URL:
#     DATABASES = {
#         "default": dj_database_url.config(
#             default=DATABASE_URL,
#             conn_max_age=600,
#         )
#     }
# else:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": BASE_DIR / "db.sqlite3",
#         }
#     }

# # =========================
# # AUTH
# # =========================
# AUTH_USER_MODEL = "accounts.User"

# AUTH_PASSWORD_VALIDATORS = [
#     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
#     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
#     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
#     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
# ]

# # =========================
# # I18N
# # =========================
# LANGUAGE_CODE = "en-us"
# TIME_ZONE = "UTC"
# USE_I18N = True
# USE_TZ = True

# # =========================
# # STATIC / MEDIA
# # =========================
# STATIC_URL = "static/"
# STATIC_ROOT = BASE_DIR / "staticfiles"

# MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR / "media"

# # =========================
# # CLOUDINARY
# # (si upload direct mobile : pas obligatoire, mais OK à garder)
# # =========================

# CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME")
# CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY")
# CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET")

# if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET:
#     cloudinary.config(
#         cloud_name=CLOUDINARY_CLOUD_NAME,
#         api_key=CLOUDINARY_API_KEY,
#         api_secret=CLOUDINARY_API_SECRET,
#         secure=True,
#     )
# # ✅ Compatibilité Django 6.0 + cloudinary_storage
# STORAGES = {
#     "default": {
#         "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
#     },
#     "staticfiles": {
#         "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
#     },
# }
# # =========================
# # REST FRAMEWORK
# # =========================
# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     ),
#     "DEFAULT_PERMISSION_CLASSES": (
#         "rest_framework.permissions.IsAuthenticated",
#     ),
# }

# # =========================
# # JWT
# # =========================
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(hours=6),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
#     "ROTATE_REFRESH_TOKENS": True,
#     "BLACKLIST_AFTER_ROTATION": True,
#     "AUTH_HEADER_TYPES": ("Bearer",),
# }

# # =========================
# # SITE LINKS (Djoser)
# # =========================
# DOMAIN = os.environ.get("DOMAIN", "localhost:5173")
# SITE_NAME = os.environ.get("SITE_NAME", "TEKTAL")
# PROTOCOL = os.environ.get("PROTOCOL", ("https" if not DEBUG else "http"))

# # URL de votre page d'activation frontend
# FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://active-tektal.vercel.app")

# DJOSER = {
#     "LOGIN_FIELD": "email",
#     "USER_CREATE_PASSWORD_RETYPE": False,

#     # Activation email ON
#     "SEND_ACTIVATION_EMAIL": True,
#     "SEND_CONFIRMATION_EMAIL": False,

#     # Ces paramètres ne sont plus utilisés car vous construisez le lien manuellement
#     # mais on les garde pour éviter les erreurs Djoser
#     'ACTIVATION_URL': 'activate?uid={uid}&token={token}',
#     'PASSWORD_RESET_CONFIRM_URL': 'reset-password?uid={uid}&token={token}',
     
#     'PROTOCOL': 'https',
#     "DOMAIN": "active-tektal.vercel.app",

#     "PASSWORD_RESET_CONFIRM_RETYPE": True,

#     "SERIALIZERS": {
#         "user_create": "accounts.serializers.UserCreateSerializer",
#         "user": "accounts.serializers.UserSerializer",
#         "current_user": "accounts.serializers.UserSerializer",
#     },

#     # Emails via tes classes (Brevo)
#     "EMAIL": {
#         "activation": "accounts.djoser_emails.ActivationEmail",
#         "password_reset": "accounts.djoser_emails.PasswordResetEmail",
#     },
# }
# # =========================
# # EMAIL (Brevo API)
# # =========================

# EMAIL_FAIL_SILENTLY = False

# EMAIL_BACKEND = "accounts.email_backends.BrevoAPIEmailBackend"

# DEFAULT_FROM_EMAIL = os.environ.get(
#     "DEFAULT_FROM_EMAIL",
#     "collefall118@gmail.com"
# )
# BREVO_API_KEY = os.environ.get("BREVO_API_KEY")



# # =========================
# # CORS
# # =========================
# CORS_ALLOWED_ORIGINS = os.environ.get(
#     "CORS_ALLOWED_ORIGINS",
#     "http://localhost:5173,http://localhost:3000,https://active-tektal.vercel.app"
#     # "http://localhost:5173,http://localhost:3000"
# ).split(",")

# CORS_ALLOW_CREDENTIALS = False

# CSRF_TRUSTED_ORIGINS = [
#     "https://tektal-backend.onrender.com",
# ]

# # =========================
# # LOGGING
# # =========================
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {"console": {"class": "logging.StreamHandler"}},
#     "root": {"handlers": ["console"], "level": "INFO"},
#     "loggers": {
#         "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": False},
#         "djoser": {"handlers": ["console"], "level": "INFO", "propagate": False},
#         "accounts": {"handlers": ["console"], "level": "INFO", "propagate": False},
#     },
# }

# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
from datetime import timedelta
import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv
# import cloudinary

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# SECURITY
# =========================
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "127.0.0.1,localhost"
).split(",")

# =========================
# APPS
# =========================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",

    # Cloudinary (ordre important)
    # "cloudinary_storage",
    "django.contrib.staticfiles",
    # "cloudinary",

    # Third-party
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "djoser",
    "corsheaders",

    # Local apps
    "accounts",
    "core",
    "paths",
    "admin_panel",
]

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# =========================
# DATABASE
# =========================
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# =========================
# AUTH
# =========================
AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =========================
# I18N
# =========================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# =========================
# STATIC / MEDIA
# =========================
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# # Remplace le bloc STORAGES par ceci
# DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
# STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# # =========================
# # CLOUDINARY
# # =========================
# CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME")
# CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY")
# CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET")

# if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET:
#     cloudinary.config(
#         cloud_name=CLOUDINARY_CLOUD_NAME,
#         api_key=CLOUDINARY_API_KEY,
#         api_secret=CLOUDINARY_API_SECRET,
#         secure=True,
#     )

# =========================
# REST FRAMEWORK  ✅ une seule fois avec JWT
# =========================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

# =========================
# JWT
# =========================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# =========================
# SITE LINKS (Djoser)
# =========================
DOMAIN = os.environ.get("DOMAIN", "localhost:5173")
SITE_NAME = os.environ.get("SITE_NAME", "TEKTAL")
PROTOCOL = os.environ.get("PROTOCOL", ("https" if not DEBUG else "http"))

FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://active-tektal.vercel.app")

DJOSER = {
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": False,
    "SEND_ACTIVATION_EMAIL": True,
    "SEND_CONFIRMATION_EMAIL": False,
    'ACTIVATION_URL': 'activate?uid={uid}&token={token}',
    'PASSWORD_RESET_CONFIRM_URL': 'reset-password?uid={uid}&token={token}',
    'PROTOCOL': 'https',
    "DOMAIN": "active-tektal.vercel.app",
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "SERIALIZERS": {
        "user_create": "accounts.serializers.UserCreateSerializer",
        "user": "accounts.serializers.UserSerializer",
        "current_user": "accounts.serializers.UserSerializer",
    },
    "EMAIL": {
        "activation": "accounts.djoser_emails.ActivationEmail",
        "password_reset": "accounts.djoser_emails.PasswordResetEmail",
    },
}

# =========================
# EMAIL (Brevo API)
# =========================
EMAIL_FAIL_SILENTLY = False
EMAIL_BACKEND = "accounts.email_backends.BrevoAPIEmailBackend"
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "collefall118@gmail.com")
BREVO_API_KEY = os.environ.get("BREVO_API_KEY")

# =========================
# CORS
# =========================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://active-tektal.vercel.app",
    "https://admin-panel-gamma-liart.vercel.app",
    "https://tektal-backend.onrender.com",
]

CORS_ALLOW_CREDENTIALS = False

CSRF_TRUSTED_ORIGINS = [
    "https://tektal-backend.onrender.com",
    "https://admin-panel-gamma-liart.vercel.app",
]
# =========================
# LOGGING
# =========================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": False},
        "djoser": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "accounts": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"