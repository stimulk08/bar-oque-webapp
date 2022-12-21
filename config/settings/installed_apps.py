from config.settings import DEBUG


DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
]

APPS = [
    'apps.kabak',
]

THIRD_PARTY_APPS = [
    'django_extensions',
    'corsheaders',
    'rest_framework',
]

DEBUG_APPS = [
    'django.contrib.staticfiles',
    'drf_spectacular',
]

PROD_APPS = [
    'whitenoise.runserver_nostatic',
]

INSTALLED_APPS = DJANGO_APPS + APPS + THIRD_PARTY_APPS + \
                 DEBUG_APPS if DEBUG else PROD_APPS
