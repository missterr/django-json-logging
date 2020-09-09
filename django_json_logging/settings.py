from django.conf import settings

LOGGING_APP_NAME = getattr(settings, 'LOGGING_APP_NAME', None)
assert LOGGING_APP_NAME, 'LOGGING_APP_NAME settings parameter must be defined'

LOGGING_ENCODING = getattr(settings, 'LOGGING_ENCODING', 'utf-8')
LOGGING_DATETIME_FORMAT = getattr(settings, 'LOGGING_DATETIME_FORMAT', '%Y-%m-%d %H:%M:%S.%f')
LOGGING_USER_PROPERTY_NAME = getattr(settings, 'LOGGING_USER_PROPERTY_NAME', 'user')
LOGGING_FIELDS = getattr(settings, 'LOGGING_FIELDS',
                         ('levelname', 'name', 'module', 'process', 'thread', 'pathname', 'created'))
