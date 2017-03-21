"""
Tests for custom form fields.
Add support for custom fields defined by users.
"""

from django.test import TestCase

from formfactory import models, fields, SETTINGS
from formfactory.tests.formfactoryapp.fields import MyCustomCharField


class CustomFieldsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.field = models.FormField.objects.create(
            title="test-field",
            slug="test-field",
            field_type="MyCustomCharField",
        )

        group = models.FormFieldGroup.objects.create(
            title="Field Group 3",
            show_title=False
        )
        models.FieldGroupThrough.objects.create(
            field=cls.field, field_group=group, order=0
        )
        cls.form_object = models.Form.objects.create(
            title="Form 1",
            slug="slug-1"
        )
        models.FieldGroupFormThrough.objects.create(
            form=cls.form_object,
            field_group=group,
            order=0
        )

    def test_field_registration(self):
        self.assertIn(
            fields.formatted_field_key(
                "MyCustomCharField", MyCustomCharField.__module__),
            fields.get_registered_fields()
        )

    def test_field_used_in_form(self):
        form = self.form_object.as_form()
        self.assertIsInstance(form.fields["test-field"], MyCustomCharField)

    def test_default_django_fields_are_registered(self):
        """Test that default django fields are registered by default.
        """
        from django.forms.fields import __all__ as django_fields

        self.assertTrue(all(
            "{}-{}".format(field_class, fields.DJANGO_FIELDS_MODULE)
            in fields.get_registered_fields()
            for field_class in django_fields
        ))

    def test_some_django_fields_can_be_omitted(self):
        """It might be convenient to not have all the built-in fields
         available for selection in the CMS. Verify that fields can
         be omitted.
        """

        # Check that BooleanField is in the registered fields
        field_key = fields.formatted_field_key(
            "BooleanField", fields.DJANGO_FIELDS_MODULE
        )
        self.assertTrue(field_key in fields.get_registered_fields())

        # Verify that BooleanField can be excluded from registered fields
        SETTINGS["excluded_fields"].append("BooleanField")
        fields.auto_discover()
        self.assertFalse(field_key in fields.get_registered_fields())
