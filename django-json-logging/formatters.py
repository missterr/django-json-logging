from logging import Formatter, LogRecord

import orjson
from django.conf import settings
from django.utils import timezone

BUILTIN_ATTRS = {
    'args',
    'asctime',
    'created',
    'exc_info',
    'exc_text',
    'filename',
    'funcName',
    'levelname',
    'levelno',
    'lineno',
    'module',
    'msecs',
    'message',
    'msg',
    'name',
    'pathname',
    'process',
    'processName',
    'relativeCreated',
    'stack_info',
    'thread',
    'threadName',
}


class JSONFormatter(Formatter):
    """JSON log formatter."""

    def format(self, record: LogRecord) -> str:
        message = record.getMessage()
        extra = self.extra_from_record(record)
        json_record = self.json_record(message, extra, record)
        return self.to_json(json_record)

    def to_json(self, record: dict) -> str:
        """Converts record dict to a JSON string."""
        return str(orjson.dumps(record), 'utf-8')

    def extra_from_record(self, record: LogRecord) -> dict:
        """Returns `extra` dict you passed to logger.

        The `extra` keyword argument is used to populate the `__dict__` of
        the `LogRecord`.
        """
        return {
            attr_name: record.__dict__[attr_name]
            for attr_name in record.__dict__
            if attr_name not in BUILTIN_ATTRS
        }

    def json_record(self, message: str, extra: dict, record: LogRecord) -> dict:
        """Log record JSON formatter.

        Particular fields can be configured in settings.LOGGING_FIELDS.
        Request field is excluded because it can't be json-encoded directly.
        """
        extra['message'] = message
        extra.update({
            field: getattr(record, field) for field in settings.LOGGING_FIELDS
        })

        if 'request' in extra:
            extra['user'] = str(extra['request'].user)
            extra.pop('request', None)

        extra['server_time'] = timezone.now().strftime(
            settings.LOGGING_DATETIME_FORMAT,
        )

        if record.exc_info:
            extra['exc_info'] = self.formatException(record.exc_info)

        return extra
