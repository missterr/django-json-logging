import json

from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.utils.translation import gettext_lazy as _

from django_json_logging.serializers import ORJsonSerializer


@override_settings(LOGGING_SERIALIZER="orjson")
class ORJsonTranslationSerializerTest(TestCase):
    def setUp(self):
        self.serializer = ORJsonSerializer()

    def test_translation_proxy_serialization(self):
        """Test basic translation proxy serialization"""
        translated_message = _("Hello, World!")
        result = self.serializer.to_json({"message": translated_message})
        parsed = json.loads(result)

        self.assertEqual(parsed["message"], "Hello, World!")

    def test_validation_error_message(self):
        """Test ValidationError with translation proxy message"""
        try:
            raise ValidationError(_("Invalid input"))
        except ValidationError as e:
            result = self.serializer.to_json({"error": e.message, "message": str(e)})
            parsed = json.loads(result)

            self.assertEqual(parsed["error"], "Invalid input")
            self.assertEqual(parsed["message"], "['Invalid input']")

    def test_validation_error_message_list(self):
        """Test ValidationError with list of translation proxy messages"""
        try:
            raise ValidationError([_("First error"), _("Second error")])
        except ValidationError as e:
            result = self.serializer.to_json({"errors": e.messages, "message": str(e)})
            parsed = json.loads(result)

            self.assertIn("First error", parsed["errors"])
            self.assertIn("Second error", parsed["errors"])
