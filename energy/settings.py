"""
Django settings for energy project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------
# SECURITY SETTINGS
# ---------------------------------------------------

SECRET_KEY = 'django-insecure-aj-6(uu#j(b8=h=%%8!j+q1latw3nm)x=igecm*d3=g_ktm*t_'

DEBUG = False   # IMPORTANT for Render deployment

ALLOWED_HOSTS = [
    "energy-project-backend-ol3t.onrender.com",   # Render backend
    "energy-project-frontend.vercel.app",         # Vercel frontend
    "localhost",
    "127.0.0.1",
    ".onrender.com",
    ".vercel.app",
]

# ---------------------------------------------------
# APPLICATIONS
# ---------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',

    'Energyapp',
]

# ---------------------------------------------------
# MIDDLEWARE (CORS MUST COME FIRST)
# ---------------------------------------------------

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",     # MUST BE FIRST
    "django.middleware.common.CommonMiddleware",

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------------------------------
# URL + TEMPLATES
# ---------------------------------------------------

ROOT_URLCONF = 'energy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'energy.wsgi.application'

# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------------------------------
# PASSWORD VALIDATION
# ---------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------
# STATIC & MEDIA FILES
# ---------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------------------------------------------
# CORS / CSRF CONFIG (RENDER + VERCEL FIX)
# ---------------------------------------------------

CORS_ALLOW_ALL_ORIGINS = False   # DO NOT USE * ON RENDER

CORS_ALLOWED_ORIGINS = [
    "https://energy-project-frontend.vercel.app",
]

CSRF_TRUSTED_ORIGINS = [
    "https://energy-project-frontend.vercel.app",
    "https://energy-project-backend-ol3t.onrender.com",
]

CORS_ALLOW_CREDENTIALS = True

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

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

# ---------------------------------------------------
# DEFAULT PK FIELD TYPE
# ---------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
