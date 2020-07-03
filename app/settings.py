import os
import django_heroku
import cloudinary
import dj_database_url
from dotenv import load_dotenv


# ---------------------------------------------------------------------------- #
DEBUG = True

#Base Directory:
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dotenv config:
dotenv_file = os.path.join(BASE_DIR, '.env')
if os.path.isfile(dotenv_file):
    load_dotenv(dotenv_file)

SECRET_KEY = os.getenv('SECRET_KEY')

# Check if ENVIRONMENT is dev or prod:
ENVIRONMENT = os.getenv('ENVIRONMENT')

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.herokuapp.com']

INSTALLED_APPS = [
    'cloudinary',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'

DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

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

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static config
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_env')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET')
)

# ---------------------------- Email Server set-up --------------------------- #
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_USE_TLS = True
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')


# Production env settings
if ENVIRONMENT == 'production':
    DEBUG = False
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # This makes debugging with Heroku logs easier when DEBUG=False:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': ('%(asctime)s [%(process)d] [%(levelname)s] '
                        'pathname=%(pathname)s lineno=%(lineno)s '
                        'funcname=%(funcName)s %(message)s'),
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            }
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
            },
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }


django_heroku.settings(config=locals(), staticfiles=False, logging=False)
del DATABASES['default']['OPTIONS']['sslmode']