from logging import LogRecord

import orjson
from django.conf import settings
from django.utils import timezone
from json_log_formatter import JSONFormatter


class DefaultJSONFormatter(JSONFormatter):
    """
    Custom JSON formatter.

    Particular fields can be configured in settings.LOGGING_FIELDS.
    Request field is excluded because it can't be json-encoded directly.
    """

    json_lib = orjson
    exclude = ('request', )

    def json_record(self, message: str, extra: dict, record: LogRecord) -> dict:
        extra['message'] = message
        extra.update({
            field: getattr(record, field) for field in settings.LOGGING_FIELDS
        })

        for field in self.exclude:
            extra.pop(field, None)

        extra['server_time'] = timezone.now().strftime(
            settings.LOGGING_DATETIME_FORMAT,
        )

        if record.exc_info:
            extra['exc_info'] = self.formatException(record.exc_info)

        return extra
