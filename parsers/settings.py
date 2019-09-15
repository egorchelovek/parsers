"""
Django settings for parsers project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c$0%j0&eh(t6ihdg-yf5__c(agey^7jk2r=ac7ut!!&kev$b8z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '.pythonanywhere.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'multiselectfield',
    'background_task',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'parsers.urls'

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

WSGI_APPLICATION = 'parsers.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'parsers',
        'USER': 'egor',
        'PASSWORD':'qwerty',
        'HOST':'localhost',
        'PORT':'',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOGIN_REDIRECT_URL = '/'

# E-mail preferences
# via SMTP
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST_USER = 'egor.zamotaev@mail.ru'
EMAIL_HOST_PASSWORD = 'DSO003LaDla'

EMAIL_SUBJECT = "Информация по аренде/продаже квартир"
EMAIL_BODY = "Здравствуйте! Прилагаю к письму таблицу с запрошенной Вами информацией.\nС уважением,\nВаш Агент."

TABLE_HEADER = {
    'A1':'Адресс',
    'B1':'Площадь',
    'C1':'Стоимость',
    'D1':'Этаж',
    'E1':'Телефонный номер',
    'F1':'Контактное лицо',
    'G1':'Ссылка',
}

# Worker default info
SOURCE_SITES = {
    'http://www.avito.ru' : 'Avito',
    'http://www.move.ru' : 'Move',
    'http://www.arendator.ru' : 'Arendator',
    'http://www.mirkvartir.ru' : 'Mirkvartir',
    'http://www.sob.ru' : 'Sob',
    'http://www.zdanie.info' :'Zdanie',
    'http://www.moskva.gde.ru' :'MoskvaGde',
    'http://www.propokupki.ru' : 'Propokupki',
    'http://www.kvmeter.ru' : 'KvMeter',
    'http://www.comrent.ru' : 'Comrent',
}

SOURCE_PAGES_SELL = {
    'Avito' : '/barnaul/kvartiry/prodam?user=1'
}

SOURCE_PAGES_RENT = {
    'Avito' : '/barnaul/kvartiry/sdam?user=1'
}

OBJECTS_AMOUNTS = {
    10:10,
    20:20,
    30:30,
    50:50,
    100:100,
}

OBJECTS_TYPES = {
    0:"Rent",
    1:"Sell",
}

UPDATING_PERIODS = {
    900 : '15 min',
    3600 : '1 hour',
    10800 : '3 hours',
    86400 : '1 day',
}

MAX_SCROLLS = 5
