from settings.base import *


DEBUG = os.getenv('DEBUG') == 'True'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS_DEV')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}