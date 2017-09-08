import warnings

from django.test import TestCase

from formfactory.decorators import generic_deprecation


class DeprecationTestCase(TestCase):
    def test_generic_deprecation(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Define empty method to attach decorator to.
            @generic_deprecation("generic_deprecation_message")
            def wrapped_method():
                pass

            # Call decorated method.
            wrapped_method()

            # Check that we do indeed have one warning.
            assert len(w) == 1

            # Check the type of warning is the default DeprecationWarning.
            assert issubclass(w[-1].category, DeprecationWarning)

            # Check that the message is actually displayed on warning.
            assert "generic_deprecation_message" in str(w[-1].message)
