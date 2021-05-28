"""
Django settings for beerbnb project.
Generated by 'django-admin startproject' using Django 3.2.
For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib     import Path
<<<<<<< HEAD
from my_settings import DATABASES, SECRET_KEY, MY_AWS_ACCESS_KEY_ID, MY_AWS_SECRET_ACCESS_KEY, EMAIL
=======
from my_settings import DATABASES, SECRET_KEY, MY_AWS_ACCESS_KEY_ID, MY_AWS_SECRET_ACCESS_KEY

>>>>>>> f5972cb... upload
# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY

#AWS S3
AWS_ACCESS_KEY_ID = MY_AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = MY_AWS_SECRET_ACCESS_KEY
AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

AWS_REGION = "ap-northeast-2"
AWS_STORAGE_BUCKET_NAME = "beerbnb"
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME,AWS_REGION)


STATIC_DEFAULT_ACL = 'public-read'
STATIC_LOCATION = 'static/'
STATIC_URL = 'https://%s/%s' % (AWS_S3_CUSTOM_DOMAIN, STATIC_LOCATION)

MEDIA_DEFAULT_ACL = 'public-read'
MEDIA_LOCATION = 'media/'
MEDIA_URL = 'https://%s/%s' % (AWS_S3_CUSTOM_DOMAIN, MEDIA_LOCATION)

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]

MEDIA_DIR = os.path.join(BASE_DIR, 'media')
MEDIAFILES_DIRS = [
    MEDIA_DIR,
]

DEFAULT_FILE_STORAGE = 'beerbnb.storages.MediaStorage' 
STATICFILES_STORAGE = 'beerbnb.storages.StaticStorage'


# SECURITY WARNING: don't run with debug turned on in production!

EMAIL_BACKEND       = EMAIL['EMAIL_BACKEND']
EMAIL_USE_TLS       = EMAIL['EMAIL_USE_TLS']
EMAIL_PORT          = EMAIL['EMAIL_PORT']
EMAIL_HOST          = EMAIL['EMAIL_HOST']
EMAIL_HOST_USER     = EMAIL['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = EMAIL['EMAIL_HOST_PASSWORD']
REDIRECT_PAGE       = EMAIL['REDIRECT_PAGE']

DEBUG = True
ALLOWED_HOSTS = ["*"]
# Application definition
INSTALLED_APPS = [
    #'django.contrib.admin',
    #'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'user',
    'room',
    'reservation',
    'storages'
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]
ROOT_URLCONF = 'beerbnb.urls'
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
WSGI_APPLICATION = 'beerbnb.wsgi.application'
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = DATABASES
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#REMOVE_APPEND_SLASH_WARNING
APPEND_SLASH = False
##CORS
CORS_ORIGIN_ALLOW_ALL=True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
		#만약 허용해야할 추가적인 헤더키가 있다면?(사용자정의 키) 여기에 추가하면 됩니다.
)