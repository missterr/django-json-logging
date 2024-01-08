import json
import logging
from io import StringIO

from django.conf import settings
from django.test import TestCase, override_settings

from django_json_logging.formatters import JSONFormatter
from django_json_logging.serializers import JsonSerializer, ORJsonSerializer, UJsonSerializer

stream = StringIO()


class JsonFormatterTestCase(TestCase):
    def setUp(self) -> None:
        self.logger = logging.getLogger("test-json-logger")
        self.logger.propagate = False
        self.handler = logging.StreamHandler(stream=stream)
        self.formatter = JSONFormatter()
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    # @patch.object(get_serializer, )
    @override_settings(LOGGING_JSON_INDENT=2)
    def test_write(self):
        """Common writing with the extra fields"""
        for serializer in (JsonSerializer, ORJsonSerializer, UJsonSerializer):
            self.formatter.serializer = serializer
            self.logger.error("Something bad happened", extra={"error_code": "xxx"})
            value = stream.getvalue().strip()
            result = json.loads(value)
            for key in settings.LOGGING_FIELDS:
                self.assertIn(key, result.keys())

            self.assertIn("error_code", result.keys())
            self.assertEqual(result["error_code"], "xxx")
            stream.seek(0)
