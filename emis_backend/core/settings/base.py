"""
Django settings for core project.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import os
from pathlib import Path

# from common.common import add_app

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'RU'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x64z@qkrb3ds#u$n=*-fb@erxkimb6s&@6hb(m_*s9(mt0dsp#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'True'
DOMAIN = os.environ.get('DOMAIN', 'localhost:8000')

ALLOWED_HOSTS = ['*']

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'content-disposition',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)

MAX_UPLOAD_SIZE = "429916160"
DATA_UPLOAD_MAX_MEMORY_SIZE = 429916160
DATA_UPLOAD_MAX_NUMBER_FIELDS = None
# FILE_UPLOAD_TEMP_DIR = f'{BASE_DIR}/temp/'
# ToDo fix load file in memory if size > 50mb
# Save to template directory
FILE_UPLOAD_MAX_MEMORY_SIZE = 429916160

# CELERY = {
#     'BROKER_URL': os.environ['CELERY_BROKER'],
#     'CELERY_IMPORTS': ('tasks', ),
#     'CELERY_TASK_SERIALIZER': 'json',
#     'CELERY_RESULT_SERIALIZER': 'json',
#     'CELERY_ACCEPT_CONTENT': ['json'],
# }

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "asgi_rabbitmq.RabbitmqChannelLayer",
#         "ROUTING": "core.routing.channel_routing",
#         "CONFIG": {
#             "url": f"amqp://{os.environ['RABBITMQ_DEFAULT_USER']}:{os.environ['RABBITMQ_DEFAULT_PASS']}@rabbitmq:5672/%2F",
#         },
#     },
# }

# Application definition
INSTALLED_APPS = [
    'modules.files_manager',
    'modules.crm',
    'modules.authentication',
    'modules.profiles',
    'modules.print_manager'
]
# add_app(f'{BASE_DIR}/modules', install_app=INSTALLED_APPS)

INSTALLED_APPS += [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'phonenumber_field',
    'phone_field',
    'core',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'debug_toolbar',
    'import_export'
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.DjangoModelPermissions'
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'common.request.RequestMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

# WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = "core.routing.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': os.environ['POSTGRES_HOST'],
        # 'PORT': os.environ['POSTGRES_PORT'],
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'profiles.CustomUser'
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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru-RU'
LANGUAGE_TRANSLATOR = 'ru'
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True
DATE_INPUT_FORMATS = ['%d.%m.%Y']
# CKEDITOR_BASEPATH = '/static/ckeditor/ckeditor/'
CKEDITOR_UPLOAD_PATH = 'static/img/'
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage',  # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
        'stylesSet': [
            {
                "name": 'Выполняем работы',
                "element": 'li',
                "attributes": {'class': 'site-feature'},
            },
            {
                "name": 'Не выполняем работы',
                "element": 'li',
                "attributes": {'class': 'site-feature not-include'},
            },
            {
                "name": 'Стиль для колонки тарифов',
                "element": 'ul',
                "attributes": {'class': 'site-type-card'},
            },
        ],
        'contentsCss': '/static/css/edit.css',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, f'static/'),
    os.path.join(BASE_DIR, f'modules/manager/static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, f'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, f'media')

FILEBROWSER_SHOW_IN_DASHBOARD = True
FILEBROWSER_MEDIA_ROOT = MEDIA_ROOT
FILEBROWSER_MEDIA_URL = MEDIA_URL
FILEBROWSER_STATIC_ROOT = STATIC_ROOT
FILEBROWSER_STATIC_URL = STATIC_URL
URL_FILEBROWSER_MEDIA = STATIC_URL + 'filebrowser/'
PATH_FILEBROWSER_MEDIA = STATIC_ROOT + 'filebrowser/'
FILEBROWSER_EXTENSIONS = {
    'Image': ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
    'Document': ['.pdf', '.doc', '.rtf', '.txt', '.xls', '.csv'],
    'Video': ['.mov', '.wmv', '.mpeg', '.mpg', '.avi', '.rm'],
    'Audio': ['.mp3', '.mp4', '.wav', '.aiff', '.midi', '.m4p'],
    'Web': ['.html', '.css', '.js'],
}
LOGIN_URL = '/admin/'

if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'logs/error.log',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }

FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler"
]

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL') == 'True'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_ADMIN_CRM = os.environ.get('EMAIL_ADMIN_CRM')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_TRUSTED_ORIGINS = ['https://api-test.emis.su', 'https://api.emis.su', 'http://localhost:3000']
