from django.test import TestCase

from formfactory import validators
from formfactory.tests.test_base import load_fixtures


class ValidatorTestCase(TestCase):
    def setUp(self):
        load_fixtures(self)

    def test_registry(self):
        self.assertIn(
            self.dummy_validator, validators.get_registered_validators()
        )

    def test_unregistry(self):
        validator = validators.get_registered_validators()[
            self.dummy_validator
        ]
        validators.unregister(validator)
        self.assertNotIn(
            self.dummy_validator, validators.get_registered_validators()
        )

    def test_validator(self):
        validator = validators.get_registered_validators()[
            self.dummy_validator
        ]
        self.assertTrue(validator(2))


class ValidatorUseCaseTest(TestCase):
    """Test the validator in action.
    """
    def setUp(self):
        pass

    def test_validation_error_raised(self):
        pass
