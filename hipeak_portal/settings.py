from pathlib import Path
import os
import collections.abc

from django.contrib import staticfiles
import django
from django.conf.global_settings import SESSION_COOKIE_AGE
from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str


try:
    from .local_settings import *
except ImportError:
    from .local_settings_variable import *


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
            'hipeak-portal.herokuapp.com',
            'localhost',
            '127.0.0.1'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'my_profile.apps.MyProfileConfig',
    'tours.apps.ToursConfig',
    'contacts.apps.ContactsConfig',
    'registration_authorisation.apps.RegistrationAuthorisationConfig',
    'equipment_stores.apps.EquipmentStoresConfig',
    'news_blog.apps.NewsBlogConfig',
    'main.apps.MainPageConfig',
    'search.apps.SearchConfig',
    'telegram_bot.apps.TelegramBotConfig',
    'captcha',
    'social_django',
    'phonenumber_field',
    'haystack',
    'django_filters',
    'bootstrapform',
    'rest_framework',
    'storages'
]

#  AWS S3 settings for HEROKU
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_URL = os.environ.get('AWS_URL')

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_MEDIA_URL = "{}/{}/".format(AWS_URL, AWS_STORAGE_BUCKET_NAME)

MEDIA_URL = AWS_MEDIA_URL

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

ROOT_URLCONF = 'hipeak_portal.urls'

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

WSGI_APPLICATION = 'hipeak_portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'uk'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DATE_INPUT_FORMATS = ['%d-%m-%Y']


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
# MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/auth/login/google-oauth2/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = "/login"
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
SOCIAL_AUTH_URL_NAMESPACE = 'social'
AUTH_USER_MODEL = 'registration_authorisation.User'

# SMTP Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.ukr.net'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
HIPEAK_EMAIL = 'hipeak.portal@gmail.com'
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Google reCAPCHA
RECAPTCHA_DEFAULT_ACTION = "generic"
RECAPTCHA_SCORE_THRESHOLD = 0.5


# HAYSTACK ELASTICSEARC SEARCH SETTINGS
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 1


RATING_CHOICE = (
        (1, "Ok"),
        (2, "Fine"),
        (3, "Good"),
        (4, "Nice"),
        (5, "Amazing")
    )

BOT_URL = "https://api.telegram.org/bot%s/" % BOT_TOKEN


SESSION_AGE = SESSION_COOKIE_AGE
