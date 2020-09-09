from logging import Formatter, LogRecord

import orjson

from django_json_logging import settings


class JSONFormatter(Formatter):
    """JSON log formatter."""

    datefmt = settings.LOGGING_DATETIME_FORMAT

    @staticmethod
    def to_json(dict_record: dict) -> str:
        """Converts record dict to a JSON string.

        The library orjson returns a bytes not an str.
        """
        return str(orjson.dumps(dict_record), settings.LOGGING_ENCODING)

    @staticmethod
    def add_user(record: LogRecord) -> LogRecord:
        """Adds `user` property from request to a LogRecord if exists."""
        if getattr(record, 'request', None):
            setattr(record, settings.LOGGING_USER_PROPERTY_NAME, str(record.request.user))
        return record

    def format(self, record: LogRecord) -> str:
        """Format the specified record as text."""
        if 'asctime' in settings.LOGGING_FIELDS:
            record.asctime = self.formatTime(record, self.datefmt)

        record = self.add_user(record)
        message = record.getMessage()
        dict_record = self.to_dict(message, record)
        return self.to_json(dict_record)

    def to_dict(self, message: str, record: LogRecord) -> dict:
        """Log record JSON formatter.

        Particular fields can be configured in settings.LOGGING_FIELDS.
        Request field is excluded because it can't be json-encoded directly.
        """
        dict_record = {'message': message, 'app_name': settings.LOGGING_APP_NAME}
        dict_record.update({
            field: getattr(record, field) for field in settings.LOGGING_FIELDS
        })

        if 'request' in dict_record:
            json_record.pop('request', None)

        if record.exc_info:
            dict_record['exc_info'] = self.formatException(record.exc_info)

        return dict_record
