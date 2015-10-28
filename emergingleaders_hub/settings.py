"""
Django settings for emergingleaders_hub project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os

import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'REPLACEME')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', True)

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    # admin
    'grappelli',
    'django.contrib.admin',
    # core
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.postgres',
    # 3rd party
    'raven.contrib.django.raven_compat',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    # us
    'operations',
    'trainings',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'emergingleaders_hub.urls'

WSGI_APPLICATION = 'emergingleaders_hub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get(
            'DATABASE_URL',
            'postgis://postgres:@localhost/emergingleaders_hub')),
}

DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')
GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# TEMPLATE_CONTEXT_PROCESSORS = (
#     "django.core.context_processors.request",
# )

# Sentry configuration
# RAVEN_CONFIG = {
#     # DevOps will supply you with this.
#     'dsn': os.environ.get('ELHUB_SENTRY_DSN', ""),
# }

# REST Framework conf defaults
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGINATE_BY': 500,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}

# Celery configuration options
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

BROKER_URL = os.environ.get('BROKER_URL', 'redis://localhost:6379/0')

from kombu import Exchange, Queue

CELERY_DEFAULT_QUEUE = 'emergingleaders_hub'
CELERY_QUEUES = (
    Queue('emergingleaders_hub',
          Exchange('emergingleaders_hub'),
          routing_key='emergingleaders_hub'),
)
CELERY_CREATE_MISSING_QUEUES = True
CELERY_ROUTES = {
    'celery.backend_cleanup': {
        'queue': 'mediumpriority',
    }
}

CELERY_ALWAYS_EAGER = False

# Tell Celery where to find the tasks
CELERY_IMPORTS = (
    'operations.tasks',
    'trainings.tasks',
)

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

import djcelery
djcelery.setup_loader()

VUMI_API_URL = \
    os.environ.get('EMERGINGLEADERS_HUB_VUMI_API_URL',
                   'http://example.com/api/v1/go/http_api_nostream')
VUMI_ACCOUNT_KEY = \
    os.environ.get('EMERGINGLEADERS_HUB_VUMI_ACCOUNT_KEY', 'acc-key')
VUMI_CONVERSATION_KEY = \
    os.environ.get('EMERGINGLEADERS_HUB_VUMI_CONVERSATION_KEY', 'conv-key')
VUMI_ACCOUNT_TOKEN = \
    os.environ.get('EMERGINGLEADERS_HUB_VUMI_ACCOUNT_TOKEN', 'conv-token')

FEEDBACK_USSD_NUMBER = \
    os.environ.get('EMERGINGLEADERS_HUB_FEEDBACK_USSD_NUMBER',
                   "*120*8864*xxxx")
FEEDBACK_MESSAGE_DELAY = \
    os.environ.get('EMERGINGLEADERS_HUB_FEEDBACK_MESSAGE_DELAY', 24)  # hours
FEEDBACK_MESSAGE = \
    os.environ.get('EMERGINGLEADERS_HUB_FEEDBACK_MESSAGE',
                   "Please help us improve Emerging Leaders Training \
                   by providing feedback on the training you received. \
                   Dial %s to provide your feedback!" % FEEDBACK_USSD_NUMBER)

try:
    from emergingleaders_hub.local_settings import *  # flake8: noqa
except ImportError:
    pass
