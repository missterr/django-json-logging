import json

from django_json_logging import settings

try:
    import ujson
except ImportError:  # pragma: nocover
    ujson = None  # type: ignore

try:
    import orjson
except ImportError:  # pragma: nocover
    orjson = None  # type: ignore


class ORJsonSerializer:

    @staticmethod
    def to_json(dict_record: dict) -> str:
        """Converts record dict to a JSON string.

        The library orjson returns a bytes not an str.
        """
        assert orjson is not None, 'orjson must be installed to use ORJsonSerializer'

        if settings.DEVELOP:
            json = orjson.dumps(dict_record, option=orjson.OPT_INDENT_2)
        else:
            json = orjson.dumps(dict_record)
        return str(json, settings.LOGGING_ENCODING)


class UJsonSerializer:
    @staticmethod
    def to_json(dict_record: dict) -> str:
        """Converts record dict to a JSON string.

        The library ujson returns a bytes not an str.
        """
        assert ujson is not None, 'ujson must be installed to use UJsonSerializer'

        if settings.DEVELOP:
            json = ujson.dumps(dict_record, ensure_ascii=False, indent=2)
        else:
            json = ujson.dumps(dict_record, ensure_ascii=False)
        return str(json, settings.LOGGING_ENCODING)


class JsonSerializer:
    @staticmethod
    def to_json(dict_record: dict) -> str:
        """Converts record dict to a JSON string.

        Using standard json library.
        """

        if settings.DEVELOP:
            return json.dumps(dict_record, ensure_ascii=False, indent=2)
        else:
            return json.dumps(dict_record, ensure_ascii=False)


def get_serializer():
    mapping = {
        'orjson': ORJsonSerializer,
        'ujson': UJsonSerializer,
        'json': JsonSerializer,
    }
    assert settings.LOGGING_SERIALIZER in mapping, 'LOGGING_SERIALIZER must be "orjson", "ujson" or "json"'
    return mapping[settings.LOGGING_SERIALIZER]
