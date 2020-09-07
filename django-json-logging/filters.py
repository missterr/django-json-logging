from logging import Filter, LogRecord

from django.conf import settings


class AppNameFilter(Filter):
    """Logging filter that adds app_name field to each log record."""

    def filter(self, record: LogRecord) -> int:
        record.app_name = settings.LOGGING_APP_NAME
        return True
