from django.test import TestCase

from formfactory import models


class CustomErrorMessageTestCase(TestCase):

    def test_custom_error_message(self):
        field = models.FormField.objects.create(
            title="Number",
            slug="number",
            field_type="django.forms.fields.IntegerField",
        )

        # Add custom error message and add it to field
        error_message = models.CustomErrorMessage.objects.create(
            key="required",
            value="Please do not leave this field empty."
        )
        field.error_messages.add(error_message)

        group = models.FormFieldGroup.objects.create(
            title="Test field group",
            show_title=False
        )
        models.FieldGroupThrough.objects.create(
            field=field, field_group=group, order=0
        )
        form = models.Form.objects.create(
            title="Form 1",
            slug="slug-1"
        )
        models.FieldGroupFormThrough.objects.create(
            form=form,
            field_group=group,
            order=0
        )
        bound_form = form.as_form(data={"number": ""})
        self.assertFalse(bound_form.is_valid())
        self.assertEqual(
            bound_form.errors["number"][0],
            "Please do not leave this field empty."
        )
