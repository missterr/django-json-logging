from logging import Formatter, LogRecord

import orjson

from django_json_logging import settings


class JSONFormatter(Formatter):
    """JSON log formatter."""

    datefmt = settings.LOGGING_DATETIME_FORMAT

    @staticmethod
    def to_json(record: dict) -> str:
        """Converts record dict to a JSON string.

        The library orjson returns a bytes not an str.
        """
        return str(orjson.dumps(record), settings.LOGGING_ENCODING)

    def format(self, record: LogRecord) -> str:
        """Format the specified record as text."""
        if 'asctime' in settings.LOGGING_FIELDS:
            record.asctime = self.formatTime(record, self.datefmt)

        message = record.getMessage()
        json_record = self.to_json_record(message, record)
        return self.to_json(json_record)

    def to_json_record(self, message: str, record: LogRecord) -> dict:
        """Log record JSON formatter.

        Particular fields can be configured in settings.LOGGING_FIELDS.
        Request field is excluded because it can't be json-encoded directly.
        """
        json_record = {'message': message, 'app_name': settings.LOGGING_APP_NAME}
        json_record.update({
            field: getattr(record, field) for field in settings.LOGGING_FIELDS
        })

        if 'request' in json_record:
            json_record['user'] = str(json_record['request'].user)
            json_record.pop('request', None)

        if record.exc_info:
            json_record['exc_info'] = self.formatException(record.exc_info)

        return json_record
