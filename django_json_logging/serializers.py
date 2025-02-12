import json
from functools import lru_cache, partial
from typing import Callable, Union

from django_json_logging import settings

try:
    import ujson
except ImportError:  # pragma: nocover
    ujson = None  # type: ignore

try:
    import orjson
except ImportError:  # pragma: nocover
    orjson = None  # type: ignore


def default(obj):
    """A callback for not serializable objects."""
    if hasattr(obj, "__str__"):
        return str(obj)
    raise TypeError


class ORJsonSerializer:
    options = {
        "LOGGING_JSON_INDENT": getattr(orjson, "OPT_INDENT_2", 0) if settings.LOGGING_JSON_INDENT else 0,
        "LOGGING_OPT_NON_STR_KEYS": getattr(orjson, "OPT_NON_STR_KEYS", 0),
        "LOGGING_OPT_APPEND_NEWLINE": getattr(orjson, "OPT_APPEND_NEWLINE", 0),
        "LOGGING_OPT_NAIVE_UTC": getattr(orjson, "OPT_NAIVE_UTC", 0),
        "LOGGING_OPT_OMIT_MICROSECONDS": getattr(orjson, "OPT_OMIT_MICROSECONDS", 0),
        "LOGGING_OPT_PASSTHROUGH_DATACLASS": getattr(orjson, "OPT_PASSTHROUGH_DATACLASS", 0),
        "LOGGING_OPT_PASSTHROUGH_DATETIME": getattr(orjson, "OPT_PASSTHROUGH_DATETIME", 0),
        "LOGGING_OPT_SERIALIZE_DATACLASS": getattr(orjson, "OPT_SERIALIZE_DATACLASS", 0),
        "LOGGING_OPT_SERIALIZE_NUMPY": getattr(orjson, "OPT_SERIALIZE_NUMPY", 0),
        "LOGGING_OPT_SERIALIZE_UUID": getattr(orjson, "OPT_SERIALIZE_UUID", 0),
        "LOGGING_OPT_SORT_KEYS": getattr(orjson, "OPT_SORT_KEYS", 0),
        "LOGGING_OPT_STRICT_INTEGER": getattr(orjson, "OPT_STRICT_INTEGER", 0),
        "LOGGING_OPT_UTC_Z": getattr(orjson, "OPT_UTC_Z", 0),
    }

    @staticmethod
    @lru_cache()
    def dumps() -> Callable:
        option = False
        for key, val in ORJsonSerializer.options.items():
            if getattr(settings, key):
                option = option | ORJsonSerializer.options[key]
        return partial(orjson.dumps, option=option) if option else orjson.dumps

    @classmethod
    def to_json(cls, dict_record: dict) -> str:
        """Converts record dict to a JSON string.

        The library orjson returns a bytes not an str.
        """
        assert orjson is not None, "orjson must be installed to use ORJsonSerializer"
        return str(cls.dumps()(dict_record, default=default), settings.LOGGING_ENCODING)


class UJsonSerializer:
    @staticmethod
    def to_json(dict_record: dict) -> str:
        """Converts record dict to a JSON string.

        The library ujson returns a bytes not an str.
        """
        assert ujson is not None, "ujson must be installed to use UJsonSerializer"
        options = {"escape_forward_slashes": False, "ensure_ascii": False, "indent": settings.LOGGING_JSON_INDENT}
        return ujson.dumps(dict_record, **options)


class JsonSerializer:
    @staticmethod
    def to_json(dict_record: dict) -> str:
        """Converts record dict to a JSON string.

        Using standard json library.
        """
        options = {"ensure_ascii": False}
        if settings.LOGGING_JSON_INDENT:
            options.update(indent=settings.LOGGING_JSON_INDENT)
        return json.dumps(dict_record, **options)


def get_serializer(
    serializer: str = settings.LOGGING_SERIALIZER,
) -> Union[ORJsonSerializer, UJsonSerializer, JsonSerializer]:
    mapping = {
        "orjson": ORJsonSerializer,
        "ujson": UJsonSerializer,
        "json": JsonSerializer,
    }
    assert serializer in mapping, 'LOGGING_SERIALIZER must be "orjson", "ujson" or "json"'
    return mapping[serializer]
