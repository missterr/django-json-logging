import json
import logging
from decimal import Decimal
from io import StringIO

from django.conf import settings
from django.test import TestCase

from django_json_logging.formatters import JSONFormatter
from django_json_logging.serializers import JsonSerializer, ORJsonSerializer, UJsonSerializer


class JsonFormatterTestCase(TestCase):
    def setUp(self) -> None:
        self.logger = logging.getLogger("test-json-logger")
        self.logger.propagate = False

    def test_write(self):
        """Common writing with the extra fields"""
        cases = (("json", JsonSerializer), ("orjson", ORJsonSerializer), ("ujson", UJsonSerializer))
        for name, serializer in cases:
            with self.subTest(name):
                stream = StringIO()
                handler = logging.StreamHandler(stream=stream)
                formatter = JSONFormatter()
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)

                extra = {
                    "int": 12,
                    "float": 12.2,
                    "list": [1, 2, 3],
                    "tuple": (1, 2, 3),
                    "string": "Some string",
                    "dict": {"qwe": 1, "da": 2},
                    "boolean": True,
                }
                self.logger.error("Something bad happened", extra=extra)

                result = json.loads(stream.getvalue())
                for key in settings.LOGGING_FIELDS:
                    self.assertIn(key, result.keys())

                for key in extra.keys():
                    self.assertIn(key, result.keys())

                self.assertEqual(result["msg"], "Something bad happened")
                self.assertEqual(result["string"], "Some string")
