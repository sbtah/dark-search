import os
from pathlib import Path
from celery.schedules import crontab
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = bool(int(os.environ.get("DEBUG", 0)))
ALLOWED_HOSTS = list(os.environ.get('ALLOWED_HOSTS', '*'))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'domains',
    'tasks',
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
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SCOUT_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SCOUT_DATABASE", os.path.join(BASE_DIR / "db.sqlite3")),
        "USER": os.environ.get("SCOUT_USER", "user"),
        "PASSWORD": os.environ.get("SCOUT_PASSWORD", "password"),
        "HOST": os.environ.get("SCOUT_HOST", "localhost"),
        "PORT": os.environ.get("SCOUT_PORT", "5432"),
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Celery settings
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER', 'redis://school-redis:6379/0')
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND", "redis://school-redis:6379/0")


tasks_acks_late = True


CELERY_BEAT_SCHEDULE = {
    'crawling-task': {
        'task': 'tasks.tasks.crawling_task',
        'schedule': timedelta(seconds=30),
    },
    'reactivate-finished': {
        'task': 'tasks.tasks.reactivate_finished',
        'schedule': timedelta(hours=12),
    },
    'reactivate-taken': {
        'task': 'tasks.tasks.reactivate_taken',
        'schedule': timedelta(hours=2),
    },
}