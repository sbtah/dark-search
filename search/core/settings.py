import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*rk37=k0dxmser27g62ph%vzz)*62f#l93o)po$fivff0is=sb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'tasks',
    'parameters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SEARCH_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SEARCH_DATABASE", os.path.join(BASE_DIR / "db.sqlite3")),
        "USER": os.environ.get("SEARCH_USER", "user"),
        "PASSWORD": os.environ.get("SEARCH_PASSWORD", "password"),
        "HOST": os.environ.get("SEARCH_HOST", "localhost"),
        "PORT": os.environ.get("SEARCH_PORT", "5432"),
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
DATE_INPUT_FORMATS = ['%d-%m-%Y %H:%M']
PROJECT_DATE_FORMAT = '%d-%m-%Y %H:%M'
USE_L10N = False
USE_I18N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery settings
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND", "redis://redis:6379/0")
CELERY_BEAT_SCHEDULE = {}
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True


# API Settings:
API_KEY = os.environ.get('API_KEY')
API_BASE_URL = os.environ.get('API_BASE_URL')

API_POST_RESPONSE_ENDPOINT = os.environ.get('API_POST_RESPONSE_ENDPOINT')
API_POST_SUMMARY_ENDPOINT = os.environ.get('API_POST_SUMMARY_ENDPOINT')
