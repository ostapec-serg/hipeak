from pathlib import Path
import os

from django.contrib import staticfiles

try:
    from .local_settings import *
except ImportError:
    pass


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
    'captcha',
    # 'snowpenguin.django.recaptcha3',
    'social_django',
    'phone_field',
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#
# STATIC_URL = '/static/'
#
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static')
# ]


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


LOGIN_URL = '/auth/login/google-oauth2/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = "/login"


# SMTP Configuration

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.ukr.net'
EMAIL_PORT = 465
EMAIL_USE_SSL = True

# Google reCAPCHA

RECAPTCHA_DEFAULT_ACTION = "generic"
RECAPTCHA_SCORE_THRESHOLD = 0.5
# RECAPTCHA_DOMAIN = 'www.recaptcha.net'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_URL_NAMESPACE = 'social'

# HAYSTACK SEARCH SETTINGS
