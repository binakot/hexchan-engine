import os
from pathlib import Path

# Paths
SETTINGS_PATH = Path(__file__).resolve()
BASE_DIR = SETTINGS_PATH.parents[1]
STORAGE_DIR = BASE_DIR / '..' / 'dev'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cl-x4wji(%=&43=*tla3+n-)vr4220%(_tiwh&@^(=dyw*=r2x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
INTERNAL_IPS = ['127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project apps
    'imageboard',
    'assets',
    'captcha',
    'client_errors',

    # Third party
    'debug_toolbar',
]

# Middleware
MIDDLEWARE = [
    # Third party
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLs
ROOT_URLCONF = 'gensokyo.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Django processors
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',

                # App processors
                'imageboard.context_processors.config',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'gensokyo.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(STORAGE_DIR / 'db.sqlite3'),
    }
}

# Password validation
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

# Internationalization and time
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = str(STORAGE_DIR / 'static')

# Uploads
MEDIA_URL = '/media/'
MEDIA_ROOT = str(STORAGE_DIR / 'upload')

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    #     'LOCATION': str(STORAGE_DIR / 'cache'),
    #     'TIMEOUT': 60 * 60,  # 1 hour
    #     'OPTIONS': {
    #         'MAX_ENTRIES': 10000
    #     }
    # },
}

# Session
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_FILE_PATH = str(STORAGE_DIR / 'session')
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 days in seconds


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base': {
            'format': '{levelname} -- {asctime} -- {message}',
            'style': '{',
        },
    },
    'handlers': {
        'server_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': str(STORAGE_DIR / 'log' / 'server_errors.log'),
            'formatter': 'base',
        },
        'client_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': str(STORAGE_DIR / 'log' / 'client_errors.log'),
            'formatter': 'base',
        },
        'security_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': str(STORAGE_DIR / 'log' / 'security_errors.log'),
            'formatter': 'base',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['server_errors'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security.*': {
            'handlers': ['security_errors'],
            'propagate': True,
        },
        'client_errors': {
            'handlers': ['client_errors'],
            'propagate': True,
        }
    },
}
