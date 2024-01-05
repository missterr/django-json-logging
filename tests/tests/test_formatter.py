import json
import logging
from io import StringIO
from unittest import TestCase

from django.conf import settings

from django_json_logging.formatters import JSONFormatter

stream = StringIO()


class JsonFormatterTestCase(TestCase):
    def setUp(self) -> None:
        self.logger = logging.getLogger("test-json-logger")
        self.handler = logging.StreamHandler(stream=stream)
        self.handler.setFormatter(JSONFormatter())
        self.logger.addHandler(self.handler)

    def test_write(self):
        """Common writing with the extra fields"""
        self.logger.error("Something bad happened", extra={"error_code": "xxx"})
        result = json.loads(stream.getvalue())
        for key in settings.LOGGING_FIELDS:
            self.assertIn(key, result.keys())

        self.assertIn("error_code", result.keys())
        self.assertEqual(result["error_code"], "xxx")
