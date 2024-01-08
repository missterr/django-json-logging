from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

try:
    getattr(settings, "LOGGING_APP_NAME", None)
except ImproperlyConfigured:
    settings.configure()


LOGGING_APP_NAME = getattr(settings, "LOGGING_APP_NAME", "Default")

LOGGING_ENCODING = getattr(settings, "LOGGING_ENCODING", "utf-8")
LOGGING_SERIALIZER = getattr(settings, "LOGGING_SERIALIZER", "json")
LOGGING_JSON_INDENT = getattr(settings, "LOGGING_JSON_INDENT", 0)
assert isinstance(LOGGING_JSON_INDENT, int), "LOGGING_JSON_INDENT should be an int"

LOGGING_DATETIME_FORMAT = getattr(settings, "LOGGING_DATETIME_FORMAT", "%Y-%m-%d %H:%M:%S.%f")
LOGGING_FIELDS = getattr(
    settings, "LOGGING_FIELDS", ("levelname", "name", "module", "process", "thread", "pathname", "created")
)
DEVELOP = getattr(settings, "DEVELOP", False)

# Orjson options
LOGGING_OPT_NON_STR_KEYS = getattr(settings, "LOGGING_OPT_NON_STR_KEYS", False)
LOGGING_OPT_INDENT_2 = getattr(settings, "LOGGING_OPT_INDENT_2", False)
LOGGING_OPT_APPEND_NEWLINE = getattr(settings, "LOGGING_OPT_APPEND_NEWLINE", False)
LOGGING_OPT_NAIVE_UTC = getattr(settings, "LOGGING_OPT_NAIVE_UTC", False)
LOGGING_OPT_OMIT_MICROSECONDS = getattr(settings, "LOGGING_OPT_OMIT_MICROSECONDS", False)
LOGGING_OPT_PASSTHROUGH_DATACLASS = getattr(settings, "LOGGING_OPT_PASSTHROUGH_DATACLASS", False)
LOGGING_OPT_PASSTHROUGH_DATETIME = getattr(settings, "LOGGING_OPT_PASSTHROUGH_DATETIME", False)
LOGGING_OPT_SERIALIZE_DATACLASS = getattr(settings, "LOGGING_OPT_SERIALIZE_DATACLASS", False)
LOGGING_OPT_SERIALIZE_NUMPY = getattr(settings, "LOGGING_OPT_SERIALIZE_NUMPY", False)
LOGGING_OPT_SERIALIZE_UUID = getattr(settings, "LOGGING_OPT_SERIALIZE_UUID", False)
LOGGING_OPT_SORT_KEYS = getattr(settings, "LOGGING_OPT_SORT_KEYS", False)
LOGGING_OPT_STRICT_INTEGER = getattr(settings, "LOGGING_OPT_STRICT_INTEGER", False)
LOGGING_OPT_UTC_Z = getattr(settings, "LOGGING_OPT_UTC_Z", False)
