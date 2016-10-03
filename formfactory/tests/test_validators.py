from django.test import TestCase

from formfactory import validators


class ValidatorTestCase(TestCase):
    def setUp(self):
        self.validator = "formfactory.tests.validators.dummy_validator"

    def test_registry(self):
        self.assertIn(self.validator, validators.get_registered_validators())

    def test_unregistry(self):
        validator = validators.get_registered_validators()[self.validator]
        validators.unregister(validator)
        self.assertNotIn(
            self.validator, validators.get_registered_validators()
        )

    def test_action(self):
        validator = validators.get_registered_validators()[self.validator]
        self.assertTrue(validator(2))
