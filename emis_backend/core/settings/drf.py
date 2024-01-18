import re
import datetime
from core.settings.base import SECRET_KEY, DEBUG
import os

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DATE_INPUT_FORMATS': ["%d-%m-%Y", '%d.%m.%Y', '%Y-%m-%d'],
    'DATE_FORMAT': '%d.%m.%Y',
    'DATETIME_FORMAT': '%d.%m.%Y %H:%M',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=30) if DEBUG else datetime.timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=365) if DEBUG else datetime.timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False if DEBUG else True,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer', 'JWT',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': datetime.timedelta(days=1) if DEBUG else datetime.timedelta(minutes=10),
    'SLIDING_TOKEN_REFRESH_LIFETIME': datetime.timedelta(days=2) if DEBUG else datetime.timedelta(days=1),

}
