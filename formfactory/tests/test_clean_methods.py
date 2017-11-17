import uuid

from django.core.urlresolvers import reverse
from django.test import TestCase

from formfactory import models


class CleanMethodsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first_field = models.FormField.objects.create(
            title="First field",
            slug="first_field",
            field_type="django.forms.fields.CharField",
        )
        cls.second_field = models.FormField.objects.create(
            title="Second field",
            slug="second_field",
            field_type="django.forms.fields.CharField",
        )

        cls.clean_method_key = "formfactory.tests.clean_methods.check_if_values_match"
        cls.clean_method = models.CleanMethod.objects.create(
            clean_method=cls.clean_method_key
        )

        group = models.FormFieldGroup.objects.create(
            title="Field Group 3",
            show_title=False
        )
        models.FieldGroupThrough.objects.create(
            field=cls.first_field, field_group=group, order=0
        )
        models.FieldGroupThrough.objects.create(
            field=cls.second_field, field_group=group, order=1
        )
        cls.form = models.Form.objects.create(
            title="Form 1",
            slug="slug-1",
            clean_method=cls.clean_method
        )
        models.FieldGroupFormThrough.objects.create(
            form=cls.form,
            field_group=group,
            order=0
        )

    def test_clean_method_validates(self):
        bound_form = self.form.as_form(data={
            "slug-1-first_field": "abc",
            "slug-1-second_field": "123",
            "slug-1-form_id": "3",
            "slug-1-uuid": uuid.uuid4()
        })
        self.assertFalse(bound_form.is_valid())
        self.assertEqual(
            bound_form.errors["__all__"][0],
            "The values you entered are not equal."
        )
