import traceback
from logging import Formatter, LogRecord

from django_json_logging import settings
from django_json_logging.serializers import get_serializer

RECORD_ATTRIBUTES = {
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
    "message",
    "module",
    "msecs",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
}


class JSONFormatter(Formatter):
    """JSON log formatter."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.datefmt = settings.LOGGING_DATETIME_FORMAT
        self.serializer = get_serializer()

    @staticmethod
    def get_extra(record: LogRecord) -> dict:
        """Determines and separate extra fields."""
        extra_names = set(record.__dict__.keys()).difference(RECORD_ATTRIBUTES)
        return {name: getattr(record, name) for name in extra_names}

    def format(self, record: LogRecord) -> str:
        """Format the specified record as text."""
        if "asctime" in settings.LOGGING_FIELDS:
            record.asctime = self.formatTime(record, self.datefmt)

        message = record.getMessage()
        dict_record = self.to_dict(message, record)
        return self.serializer.to_json(dict_record)

    def to_dict(self, message: str, record: LogRecord) -> dict:
        """Log record JSON formatter.

        Particular fields can be configured in settings.LOGGING_FIELDS.
        Request field is excluded because it can't be json-encoded directly.
        """
        extra = self.get_extra(record)
        default = {"msg": message, "app_name": settings.LOGGING_APP_NAME}
        builtin = {field: getattr(record, field) for field in settings.LOGGING_FIELDS}
        dict_record = {**extra, **builtin, **default}

        dict_record.pop("request", None)

        if record.exc_info:
            if settings.DEVELOP:
                traceback.print_exception(*record.exc_info)
            else:
                extra["exc_info"] = self.formatException(record.exc_info)

        return dict_record
