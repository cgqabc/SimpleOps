# -*- coding: utf-8 -*-
"""
Django settings for SimpleOps project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-#e334xxs%naodb)axj#9z$w*vnwbq1&gymw$1o51&_ow3&aac'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False
# DEBUG_TOOLBAR_PATCH_SETTINGS = False
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'elfinder',
    # 'storages',
    'mfile',
    'channels',
    'chat',
    'accounts',
    'cmdb',
    'setup_jobs',
    'deploy',
    'delivery',
    'rest_framework',
    'django_celery_results',
    'django_celery_beat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SimpleOps.urls'


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
            ],
        },
    },
]


REST_FRAMEWORK = {
     'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,

}


CELERY_BROKER_URL = 'redis://127.0.0.1:6379/3'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
# CELERY_IMPORTS = ("tasks",)  #使用app.autodiscover_tasks，可备用参考

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgiref.inmemory.ChannelLayer",
        "ROUTING": "SimpleOps.routing.channel_routing",
    },
}
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'asgi_redis.RedisChannelLayer',
#         'CONFIG': {
#             'hosts': [('localhost', 6379)],
#         },
#         'ROUTING': 'accounts.routing.channel_routing',
#         # 'ROUTING': 'chat.routing.channel_routing',
#
#     }
# }

WSGI_APPLICATION = 'SimpleOps.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static').replace('\\', '/')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_ROOT = os.path.join(BASE_DIR, 'upload')
ELFINDER_DIR = os.path.join(BASE_DIR, 'upload/myfile')
MEDIA_URL = '/upload/'



LOGIN_URL = '/login/'
AUTH_USER_MODEL = 'accounts.User_info'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'ken178453063@163.com'
EMAIL_HOST_PASSWORD = 'asd321'

LOGGING = {
    'version': 1,#日志版本
    'disable_existing_loggers': False,#True：disable原有日志相关配置
    'formatters': {#日志格式
        'verbose': {#详细格式
            'format': '%%(levelname)s (asctime)s  %(filename)s %(module)s  %(message)s'
        },
        'simple': {#简单格式
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {#日志过滤器
        # 'special': {#特殊过滤器，替换foo成bar，可以自己配置
        #     '()': 'project.logging.SpecialFilter',
        #     'foo': 'bar',
        # },
        'require_debug_true': {#是否支持DEBUG级别日志过滤
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {#日志handlers
        'file': {#文件handler
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': './controller.log',
            'formatter': 'verbose'
        },
        'console': {#控制器handler，INFO级别以上的日志都要Simple格式输出到控制台
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {#邮件handler，ERROR级别以上的日志要特殊过滤后输出
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            # 'filters': ['special']
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console','file'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'myproject.custom': {
            'handlers': ['console', 'mail_admins', 'file'],
            'level': 'INFO',
            # 'filters': ['special']
        }
    }
}

