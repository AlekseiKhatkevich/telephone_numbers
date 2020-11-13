import os
from pathlib import Path

from dotenv import load_dotenv

# Загрузка переменных окружения
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

load_dotenv(Path(fr'telephone_numbers/env/default.env'), verbose=True)
load_dotenv(Path(fr'telephone_numbers/env/{ENVIRONMENT}.env'), verbose=True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv('DEBUG')))

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0.0.0.0', ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # приложения проекта
    'ascertain.apps.AscertainConfig',

    # сторонние приложения
    'rest_framework',
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

ROOT_URLCONF = 'telephone_numbers.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', ]
        ,
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

WSGI_APPLICATION = 'telephone_numbers.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DB_HOST'),
        'PORT': int(os.getenv('DB_PORT')),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'NAME': os.getenv('DB_NAME'),
        'CONN_MAX_AGE': None,
        'TEST': {
            'NAME': 'mobile_db_tests',
            'SERIALIZE': False,
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

#  Настройки Redis.
REDIS_LOCATION = os.getenv('REDIS_LOCATION')
REDIS_DEFAULT_DB = os.getenv('REDIS_DEFAULT_DB')
REDIS_CELERY_DB = os.getenv('REDIS_CELERY_DB')
REDIS_CELERY_RESULT_BACKEND_DB = os.getenv('REDIS_CELERY_RESULT_BACKEND_DB')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': fr'redis://{REDIS_LOCATION}/{REDIS_DEFAULT_DB}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        }
    }
}

#  Настройки DRF.
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'drf_ujson.renderers.UJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'drf_ujson.parsers.UJSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
}

# Logging settings
LOGFILES_DIR = Path(r'logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGFILES_DIR / 'logfile.log',
            'delay': True,
            'maxBytes': 10 ** 6,
            'backupCount': 2,
            'formatter': 'verbose',
            'level': 'WARNING',
            'encoding': 'UTF-8',
        },
        'security_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGFILES_DIR / 'security_logfile.log',
            'delay': True,
            'maxBytes': 10 ** 3,
            'backupCount': 2,
            'formatter': 'verbose',
            'level': 'WARNING',
            'encoding': 'UTF-8',
        },
        'csv_handle_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGFILES_DIR / 'csv_handle_logfile.log',
            'delay': True,
            'maxBytes': 10 ** 6,
            'backupCount': 2,
            'formatter': 'verbose',
            'level': 'INFO',
            'encoding': 'UTF-8',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console', ],
            'propagate': True,
            'level': 'WARNING',
        },
        'django.security': {
            'handlers': ['security_file', ],
            'propagate': True,
            'level': 'WARNING',
        },
        'handle_csv': {
            'handlers': ['csv_handle_file', ],
            'propagate': True,
            'level': 'INFO',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} || {asctime} || {module} || {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }, },
}

DJANGO_DB_LOGGER_ENABLE_FORMATTER = True
