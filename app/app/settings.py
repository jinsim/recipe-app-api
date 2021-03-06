"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.1.15.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1*8c5zjt5q880#x5#v9vl$-^$3^h!i8zb$k6owj=^mb#wi#3(5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "core",
    "user",
    "rest_framework",
    "rest_framework.authtoken",
    "recipe",
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

ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    # 쉽게 구성을 바꿀 수 있다.
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # host와 password 같은 것을 도커를 통해 환경 변수에 넣어놨다.
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# static 파일들은 웹서버/static에 위치할 것이다.
STATIC_URL = '/static/'
# media 경로도 추가함으로써, 미디어 파일을 업로드할 때 웹 서버를 통해 엑세스 할 수 있다.
MEDIA_URL = '/media/'

# media root는 django에게 모든 media파일을 도커 컨테이너에 저장하는 위치를 알려준다.
MEDIA_ROOT = '/vol/web/media'
# 프로젝트가 빌드될 때 모든 정적 파일들이 덤프되는 곳
STATIC_ROOT = '/vol/web/static'
# django는 collectstatic 명령어로 정적 파일들을 모은다.그리고 그를 static root에 저장한다.
# 즉 배포버전에서 프로젝트를 실행할 때, 이러한 정적 파일에 엑세스하거나 django admin을 볼 수 있다.

# django 개발 서버는 우리 프로젝트에 대한 모든 의존성에 대해 정적 파일을 제공해준다.
# 그러나 media는 제공해주지 않는다. 따라서 urls.py에 수동으로 추가해야한다.


AUTH_USER_MODEL = 'core.User'
