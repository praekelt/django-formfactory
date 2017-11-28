from django.forms import ValidationError
from django.test import TestCase

from formfactory import models, validators
from formfactory.tests.test_base import load_fixtures


class ValidatorTestCase(TestCase):
    def setUp(self):
        load_fixtures(self)

    def test_action(self):
        validator = validators.get_registered_validators()[
            self.dummy_validator
        ]
        self.assertTrue(validator(2))

    def test_form_field_validation(self):
        field = models.FormField.objects.create(
            title="Number",
            slug="number",
            field_type="django.forms.fields.IntegerField",
        )
        field.additional_validators.add(self.validator)
        group = models.FormFieldGroup.objects.create(
            title="Field Group 3",
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
        bound_form = form.as_form(data={"number": 3})
        self.assertRaises(
            ValidationError,
            lambda: bound_form.fields["number"].run_validators(3)
        )

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
