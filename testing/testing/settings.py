"""
Django settings for testing project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__) , ".env")
load_dotenv(dotenv_path)
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$txw&#8w3o6hua4fvmg&k+s8$*liu0afply$g0jnmey))is4ec'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("debug", False))

ALLOWED_HOSTS = [str(e) for e in os.environ.get("allowed_hosts").split(",")]

#Check if environment is production
PRODUCTION = bool(int(os.environ.get('prod' , 0)))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'epilogue',
    'analytics',
    'workout',
    'messaging',
    'authentication',
    'regeneration',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',   
    'rest_framework_swagger',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',   
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'request_logging.middleware.LoggingMiddleware',
    'workoutplan.exercise_workout_relation.middleware.EDRelationMiddleware'
]

ROOT_URLCONF = 'testing.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates') , ],
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

WSGI_APPLICATION = 'testing.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('dbname'),
        'USER' : os.environ.get('dbuser'),
        'PASSWORD' : os.environ.get('dbpassword'),
        'HOST' : os.environ.get('dbhost'),
        'PORT' : os.environ.get('dbport')
    }
}

if os.environ.get('database2'):
    vals = {
        "ENGINE" : 'django.db.backends.mysql',
        'NAME': os.environ.get('dbname2'),
        'USER' : os.environ.get('dbuser2'),
        'PASSWORD' : os.environ.get('dbpassword2'),
        'HOST' : os.environ.get('dbhost2'),
        'PORT' : os.environ.get('dbport2')
    }
    DATABASES.update({
        'main' : {
            **vals  
        }
    })


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ.get("time_zone")

USE_I18N = True
USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
 ]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES' : [
        'epilogue.authentication.CustomerAuthentication'
    ],
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES' : {
        'navratri-sms' : '10/day',
        'anon' : '2000/hour',
        'user' : '9000/hour'
    }
}

REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER' : 'epilogue.serializers.LoginSerializer',
    'USER_DETAILS_SERIALIZER' : 'epilogue.serializers.CustomerSerializer'
}

REST_AUTH_TOKEN_MODEL = 'epilogue.models.Token'
REST_SESSION_LOGIN = False
CORS_ORIGIN_ALLOW_ALL =  True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters' : {
        'verbose' : {
            'format' : '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple' : {
            'format' : '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'logzioFormat': {
            'format': '{"additional_field": "value"}'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename' : 'logs/debug.log'
        },
        'request': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename' : 'logs/request.log'
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/error.log',
        },
        'regeneration': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        #'filename' : 'regeneration.log'
        },
        'persister' : {
            'level' : 'DEBUG',
            'class' : 'logging.FileHandler',
            'filename' : 'logs/persister.log'
        },
        'ep_dp_relation' : {
            'level' : 'DEBUG',
            'class' : 'logging.FileHandler',
            'filename' : 'logs/ep_dp_relation.log'
        },
    },
    'loggers': {
        'django': {
            'handlers' : [ 'debug' ],
            'formatter' : 'verbose',
            'propagate': True,
        },
        'workoutplan' : {
            'handlers' : [ 'debug' ],
            'formatter' : 'verbose',
            'level' : 'DEBUG',
            'propagate' :  True
        },
        'workout' : {
            'handlers' : [ 'debug' ],
            'formatter' : 'verbose',
            'level' : 'DEBUG',
            'propagate' :  True
        },
        'epilogue' : {
            'handlers' : [ 'debug' ],
            'formatter' : 'verbose',
            'level' : 'DEBUG',
            'propagate' :  True
        },
        'regeneration' : {
            'handlers' : [ 'regeneration' ],
            'formatter' : 'verbose',
            'level' : 'DEBUG',
            'propagate' :  True
        },
        'django.request': {
            'handlers' : ['logzio' if PRODUCTION else 'request'],
            'level' : 'DEBUG',
            'propagate' : False
        },
        'persister' : {
            'handlers' : ['persister'],
            'formatter' : 'verbose',
            'level': 'DEBUG',
            'propagate' : True
        },
        'fitness_upgrade':{
            'handlers' : ['ep_dp_relation'],
            'formatters' : 'verbose',
            'level' : 'DEBUG',
            'propagate' : True
        },
        'activity_upgrade':{
            'handlers' : ['ep_dp_relation'],
            'formatters' : 'verbose',
            'level' : 'DEBUG',
            'propagate' : True
        }
    },
}

if PRODUCTION:
    LOGGING['handlers']['logzio'] = {
            'class' : 'logzio.handler.LogzioHandler',
            'level' : 'DEBUG',
            'formatter' : 'logzioFormat',
            'token' : 'OZhCQHDtZwULxKlhuPztkvwQoOwTsyWA',
            'logzio_type' : 'django',
            'logs_drain_timeout' :5,
            'url' : 'https://listener.logz.io:8071',
            'debug' : True
        }
#AWS SES Details
EMAIL_BACKEND = 'django_ses.SESBackend'

AWS_ACCESS_KEY_ID = 'AKIAIGH4FX24ZSFPKRSA' 
AWS_SECRET_ACCESS_KEY = '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'

AWS_SES_REGION_NAME = 'us-west-2'
AWS_SES_REGION_ENDPOINT = 'email-smtp.us-west-2.amazonaws.com'


EMAIL_HOST_USER="AKIAI5EL2SYGCS62IDQA"
EMAIL_HOST_PASSWORD="AqJF54BZeSJofQ+di5r3p4L5yV23JXTWLMib7BcAqO7y"
email_user_name="Ghost"
DEFAULT_FROM_USER="info@98Fit"

CACHES = {
    'default': {
                'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
                'LOCATION': '/var/tmp/django_cache',
                'TIMEOUT' : None
            }
}

CACHE_WORKOUT=False
REQUEST_LOGGING_ENABLE_COLORIZE=False
