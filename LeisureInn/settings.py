"""
Django settings for LeisureInn project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os

from pathlib import Path
from django.contrib.auth import get_user_model
import dj_database_url # package that will connect to Heroku database


"""THIS ENVIRON SETUP HERE WAS THE SOLUTION TO SECRET KEY BECOMING INVISIBLE TO CELERY AS A ENVIRONMENT VARIABLE"""
import environ
env = environ.Env()
environ.Env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


ENVIRONMENT = os.environ.get('ENVIRONMENT', default='production')

if ENVIRONMENT == 'production':
    SECURE_BROWSER_XSS_FILTER = True # protect against cross-site scripting attacks
    X_FRAME_OPTIONS = 'DENY' # to protect against clickjacking attacks
    SECURE_SSL_REDIRECT = True # make all non HTTPS traffic redirect  to HTTPS
    SECURE_HSTS_SECONDS = 3600 # [HTTP Strict Transfer Security] the time in seconds the browser should remember that this application is only accessible using HTTPS
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True # to force every subdomain to be accessible over HTTPS only
    SECURE_HSTS_PRELOAD =  True # to ensure https connection to website, before actually visiting the website
    SECURE_CONTENT_TYPE_NOSNIFF = True # 
    SESSION_COOKIE_SECURE = True # to use session cookie only over HTTPS
    CSRF_COOKIE_SECURE = True # to secure csrf cookie in HTTPS connection
    



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = ['0.0.0.0', '.herokuapp.com', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    
    # system apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # whitenoise installed app
    'django.contrib.staticfiles',
    'django.contrib.sites', # for 3rd party account site
    
    # local apps with Django Channels
    
    'channels',
    # 'chat.apps.ChatConfig',
    
    # local apps
    'pages.apps.PagesConfig',
    'rooms.apps.RoomsConfig',
    'bookings.apps.BookingsConfig',
    'payments.apps.PaymentsConfig',
    'users.apps.UsersConfig',
    'guest_reservations.apps.GuestReservationsConfig',
    'guest_chatRoom.apps.GuestChatroomConfig',
    'hotel_services.apps.HotelServicesConfig',
    
    # 3rd party apps
    'crispy_forms',
    'bootstrap4',
    'bootstrap_datepicker_plus',
    'allauth',
    'allauth.account', # a 3rd party account site
    # "pinax.messages",
    # 'webpush', # for web push notifications 
    
]

SITE_ID = 1 # number of 3rd party account site

AUTH_USER_MODEL = 'users.CustomUser'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', # django's default mode of authenticating user
    'allauth.account.auth_backends.AuthenticationBackend' # making django-allauth authentication mode default
]

# LOGIN_REDIRECT_URL = 'rooms:home'
LOGIN_REDIRECT_URL = 'users:profile-update'
ACCOUNT_LOGOUT_REDIRECT = 'rooms:home'

# EXTRA DJANGO-ALLAUTH SETTINGS
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email' # authentication method done by email
ACCOUNT_UNIQUE_EMAIL = True

ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'

ACCOUNT_SESSION_REMEMBER = True # to remember user login session

# ACCOUNT_SIGNUP_FORM_CLASS = 'users.forms.AdditionalSignUpInfoForm' # adding the additional signUp form to django-allauth
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'rooms:home' # redirect url after email confirmation
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # middleware to serve static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LeisureInn.urls'

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
                
                #3rd party context processor
                # "pinax.messages.context_processors.user_messages"
            ],
        },
    },
]

WSGI_APPLICATION = 'LeisureInn.wsgi.application'
REDIS_HOST = os.environ.get('REDIS_HOST')

#Configuration for Channels
ASGI_APPLICATION = "LeisureInn.asgi.application"
# CHANNELS LAYER CONFIGURATION
## connecting Channels to the redis server
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)], # uncomment this if below setting doesn't work'
            # "hosts": [(REDIS_HOST, 30650)] # comment this if it doesn't work'
        },
    },
}


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST':  'db',
        'PORT': 5432
    }
    
}

# database connection settings for production in Heroku
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)


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

STATICFILES_DIRS = ( os.path.join(BASE_DIR, 'static'), )
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# DJANGO CRISPY FORM PACK
CRISPY_TEMPLATE_PACK='bootstrap4'

# BOOTSTRAP TO INCLUDE J-QUERY
BOOTSTRAP4={
    'include_jquery': True,
}

# CELERY BROKER_URL TO CONNECT WITH RABBITMQ
# CELERY_BROKER_URL = "amqp://guest:guest@0.0.0.0:5672//" # [didn't work on docker container]
# CELERY_BROKER_URL = "amqp://guest:guest@rabbitmq:5672/" # [worked on docker container] # uncomment if below setting doesn't work
CELERY_BROKER_URL = os.environ.get('CLOUDAMQP_URL') # [for production]CLOUDAMQP Broker URL from Heroku, comment if if does not work
# CELERY_RESULT_BACKEND = 'rpc://localhost:5672/' # uncomment this if below doesn't work'
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_BROKER_POOL_LIMIT = 1
CELERY_RESULT_PERSISTENT = True

# EMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'leisureinnco@gmail.com' # the email sender email address


# FLUTTERWAVE KEYS
FLUTTERWAVE_TEST_SECRET_KEY = os.environ.get('FLUTTERWAVE_TEST_SECRET_KEY')
FLUTTERWAVE_TEST_PUBLIC_KEY = os.environ.get('FLUTTERWAVE_TEST_PUBLIC_KEY')

# Web Push notification settings
WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": os.environ.get('VAPID_PUBLIC_KEY'),
    "VAPID_PRIVATE_KEY": os.environ.get('VAPID_PRIVATE_KEY'),
    "VAPID_ADMIN_EMAIL": os.environ.get('VAPID_ADMIN_EMAIL')
}