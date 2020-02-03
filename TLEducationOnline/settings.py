"""
Django settings for TLEducationOnline project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# 设置为Python的搜索目录之下，不加的话，通过Mark Directory as设置为Sources Root可以直接在Pycharm编辑器内正常运行，但在命令行下会找不到相应文件而报错
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=e^f@lpwnsf^jri#!oc0z_04k(%0xp8bcrfxbdqb#!c#g6qu1q'

# SECURITY WARNING: don't run with debug turned on in production!
# 当DEBUG为TRUE时，有用，当DEBUG为FALSE时，就默认为生产环境，将不再起作用，需要自己重新配置
# 此时必须注释掉，否则会报错说它包含新配置的STATIC_ROOT
DEBUG = True

ALLOWED_HOSTS = ['*']
AUTHENTICATION_BACKENDS = ('users.views.CustomBackend',)

# Application definition
# 不注册app的话就无法通过migration生成相应的数据表
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'courses',
    'organization',
    'operation',
    'crispy_forms',
    'xadmin',
    'captcha',
    'pure_pagination',
    'DjangoUeditor',
]
AUTH_USER_MODEL = 'users.UserProfile'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TLEducationOnline.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media', # 不配置这个值的话，org_list.html中的{{ MEDIA_URL }}是取不到的
            ],
        },
    },
]

WSGI_APPLICATION = 'TLEducationOnline.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
# 连接数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tleducationonline',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1'
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

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False  #为True时使用国际时间，用False则使用本地时间


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
# 配置static目录路劲
STATIC_URL = '/static/'
# 当DEBUG为TRUE时，STATICFILES_DIRS有用，要保留。
# 当DEBUG为FALSE时，就默认为生产环境，STATICFILES_DIRS将不再起作用，需要自己重新配置STATIC_ROOT
# 此时必须将注释掉STATICFILES_DIRS，否则会报错说它包含新配置的STATIC_ROOT
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


EMAIL_HOST = 'smtp.sina.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'tonglefight@sina.com'
EMAIL_HOST_PASSWORD = 'Wuhan500274'
EMAIL_USE_TLS = True
EMAIL_FROM = 'tonglefight@sina.com'

# 图片上传文件的路径
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

