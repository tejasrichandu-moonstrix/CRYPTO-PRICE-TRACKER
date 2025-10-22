# crypto_tracker/settings.py — Django Settings for Crypto Tracker

import os
from pathlib import Path
from decouple import config

# ---------------------------
# Base directory
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------
# Security settings
# ---------------------------
SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['*']  # Change in production

# ---------------------------
# Installed apps
# ---------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tracker.apps.TrackerConfig',  # Your app
]

# ---------------------------
# Middleware
# ---------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------
# URLs and WSGI
# ---------------------------
ROOT_URLCONF = 'crypto_tracker.urls'
WSGI_APPLICATION = 'crypto_tracker.wsgi.application'

# ---------------------------
# Templates
# ---------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# ---------------------------
# Database
# ---------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------
# Password validation
# ---------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------
# Internationalization
# ---------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------
# Static files (CSS, JS, Images)
# ---------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# ---------------------------
# Default primary key type
# ---------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------
# CoinAPI settings
# ---------------------------
COINAPI_KEY = config('COINAPI_KEY', default='')
COINAPI_URL = 'https://rest.coinapi.io/v1'

# ---------------------------
# Render Deployment Auto-Config
# ---------------------------
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    DEBUG = False
