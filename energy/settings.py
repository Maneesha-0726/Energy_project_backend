from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-secret"

# -----------------------------------
# ✔ DEVELOPMENT MODE
# -----------------------------------
DEBUG = True

ALLOWED_HOSTS = ["*", "localhost", "127.0.0.1"]

# -----------------------------------
# INSTALLED APPS
# -----------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "corsheaders",
    "rest_framework",

    "Energyapp",
]

# -----------------------------------
# MIDDLEWARE
# -----------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",

    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "energy.urls"

# -----------------------------------
# TEMPLATES
# -----------------------------------
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

WSGI_APPLICATION = "energy.wsgi.application"

# -----------------------------------
# DATABASE
# -----------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# -----------------------------------
# STATIC & MEDIA
# -----------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# =====================================================
# ✔ CORS + CSRF FOR LOCAL DEVELOPMENT
# =====================================================

# Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True

# Explicitly allow React dev server
CORS_ALLOWED_ORIGINS = [
    "https://energy-project-frontend.vercel.app",
]

CSRF_TRUSTED_ORIGINS = [
    "https://energy-project-frontend.vercel.app",
]

CORS_ALLOW_CREDENTIALS = True

# Allow common headers
CORS_ALLOW_HEADERS = ["*"]
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_ORIGINS_ALL =["*"]
# Allow all methods
CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
