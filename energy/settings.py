from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-secret"

# ---------------------------
# PRODUCTION MODE
# ---------------------------
DEBUG = False

ALLOWED_HOSTS = [
    "energy-project-backend-ol3t.onrender.com",
    "energy-project-frontend.vercel.app",
    ".onrender.com",
    ".vercel.app",
    "localhost",
    "127.0.0.1",
]

# ---------------------------
# INSTALLED APPS
# ---------------------------
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

# ---------------------------
# MIDDLEWARE
# ---------------------------
MIDDLEWARE = [
    # ⭐ MUST BE AT TOP FOR CORS TO WORK
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

# ---------------------------
# TEMPLATES
# ---------------------------
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

# ---------------------------
# DATABASE
# ---------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ---------------------------
# STATIC & MEDIA
# ---------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ============================================================
# 🔥 CORS & CSRF — FINAL FIX FOR RENDER + VERCEL CONNECTION
# ============================================================

# Allow all origins (this is required for ML/YOLO file uploads)
CORS_ALLOW_ALL_ORIGINS = True

# Render free tier does not require credentials
CORS_ALLOW_CREDENTIALS = False

# Trusted origins for CSRF (Vercel + Render)
CSRF_TRUSTED_ORIGINS = [
    "https://energy-project-frontend.vercel.app",
    "https://energy-project-backend-ol3t.onrender.com",
]

# Allow headers
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# Allow methods
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

# ---------------------------
# DEFAULT
# ---------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
