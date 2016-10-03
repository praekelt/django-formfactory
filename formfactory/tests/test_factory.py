from django.test import TestCase

from formfactory import models
from formfactory.tests.test_base import load_fixtures


class FactoryTestCase(TestCase):
    def setUp(self):
        load_fixtures(self)
        self.form_factory = self.simpleform.as_form()
        self.form_data = {
            "uuid": self.form_factory.fields["uuid"].initial,
            "form_id": self.form_factory.fields["form_id"].initial,
            "salutation": "Mr",
            "name": "Name Surname",
            "email-address": "test@test.com",
            "accept-terms": True
        }

    def test_form(self):
        for value in self.simpleformfield_data.values():
            self.assertIn(value["slug"], [f for f in self.form_factory.fields])
            for k, v in value.items():
                if k in ["label", "help_text", "required"]:
                    self.assertEqual(
                        v, getattr(self.form_factory.fields[value["slug"]], k)
                    )

        form_factory = self.simpleform.as_form(data=self.form_data)
        self.assertTrue(form_factory.is_bound)
        self.assertFalse(bool(form_factory.errors))
        self.assertTrue(form_factory.is_valid())

    def test_save(self):
        form_factory = self.simpleform.as_form(data=self.form_data)
        self.assertTrue(form_factory.is_valid())

        form_factory.save()
        form_store = models.FormData.objects.get(
            uuid=form_factory.fields["uuid"].initial
        )
        for field in form_store.items.all():
            self.assertEqual(
                field.value, str(self.form_data[field.form_field.slug])
            )

    def tearDown(self):
        pass
