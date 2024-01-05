from django.utils.log import DEFAULT_LOGGING

SECRET_KEY = "fake-key"
INSTALLED_APPS = [
    "django_json_logging",
    "tests",
]

LOGGING_APP_NAME = "test-app"
LOGGING_LOGLEVEL = "INFO"
LOGGING_FIELDS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
}

LOGGING_SERIALIZER = "orjson"
LOGGING_OPT_INDENT_2 = True
LOGGING_OPT_NON_STR_KEYS = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "django_json_logging.formatters.JSONFormatter",
        },
        "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
        "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": LOGGING_LOGLEVEL,
        },
        "celery": {
            "handlers": ["console"],
            "level": LOGGING_LOGLEVEL,
        },
        "django": {
            "handlers": ["console"],
            "level": LOGGING_LOGLEVEL,
            "propagate": False,
        },
        "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
    },
}
