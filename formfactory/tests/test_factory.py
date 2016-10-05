from django.test import TestCase

from formfactory import models
from formfactory.tests.test_base import load_fixtures


class FactoryTestCase(TestCase):
    def setUp(self):
        load_fixtures(self)
        self.form_factory = self.simpleform.as_form()
        self.form_fields = self.form_factory.fields
        self.form_data = {
            "subscribe-form-uuid": self.form_fields["uuid"].initial,
            "subscribe-form-form_id": self.form_fields["form_id"].initial,
            "subscribe-form-salutation": "Mr",
            "subscribe-form-name": "Name Surname",
            "subscribe-form-email-address": "test@test.com",
            "subscribe-form-accept-terms": True
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
            field_key = "%s-%s" % (form_factory.prefix, field.form_field.slug)
            self.assertEqual(field.value, str(self.form_data[field_key]))

    def tearDown(self):
        pass
