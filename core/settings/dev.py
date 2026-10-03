from .base import *


DEBUG = os.getenv('DEBUG') == 'True'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
REST_AUTH = {
    'JWT_AUTH_SECURE': not DEBUG,  # Set to True in production (HTTPS)
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}