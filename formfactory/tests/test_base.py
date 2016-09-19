from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from formfactory import actions, models, validators


def load_fixtures(kls):
    kls.form_data = {
        "title": "Form 1",
        "slug": "form-1"
    }
    kls.form = models.Form.objects.create(**kls.form_data)

    for count, field_type in enumerate(models.FIELD_TYPES):
        setattr(kls, "formfield_data_%s" % count, {
            "title": "Form Field %s" % count,
            "position": count,
            "form": kls.form,
            "field_type": field_type,
            "label": "Form Field %s" % count,
        })
        setattr(kls, "formfield_%s" % count, models.FormField.objects.create(
            **getattr(kls, "formfield_data_%s" % count)
        ))


class TestValidator(validators.BaseValidator):
    pass


class TestAction(actions.BaseAction):
    pass


class ValidatorTestCase(TestCase):
    def setUp(self):
        self.validator = TestValidator()

    def test_registry(self):
        validators.register(self.validator)

        # ensure the class is registered as expected
        self.assertIn(self.validator, validators.get_registered_validators())

    def test_unregistry(self):
        validators.register(self.validator)

        # ensure the class is registered as expected
        self.assertIn(self.validator, validators.get_registered_validators())

        validators.unregister(self.validator)

        # ensure the class is unregistered as expected
        self.assertNotIn(self.validator, validators.get_registered_validators())


class ActionTestCase(TestCase):
    def setUp(self):
        self.action = TestAction()

    def test_registry(self):
        actions.register(self.action)

        # ensure the class is registered as expected
        self.assertIn(self.action, actions.get_registered_actions())

    def test_unregistry(self):
        actions.register(self.action)

        # ensure the class is registered as expected
        self.assertIn(self.action, actions.get_registered_actions())

        actions.unregister(self.action)

        # ensure the class is unregistered as expected
        self.assertNotIn(self.action, actions.get_registered_actions())


class ModelTestCase(TestCase):
    def setUp(self):
        load_fixtures(self)

    def test_field_constant(self):

        # ensure the field types are populated
        self.assertIn(("DateTimeField", "DateTimeField"), models.FIELD_TYPES)
        self.assertIn(("BooleanField", "BooleanField"), models.FIELD_TYPES)
        self.assertIn(("CharField", "CharField"), models.FIELD_TYPES)

    def test_form(self):

        # ensure the form model has been saved correctly
        for key, value in self.form_data.items():
            self.assertEqual(getattr(self.form, key), value)

        # ensure all form fields were saved
        self.assertEqual(self.form.fields.count(), len(models.FIELD_TYPES))

    def test_formfield(self):

        # ensure the form model has been saved correctly
        for count in range(len(models.FIELD_TYPES)):
            formfield_data = getattr(self, "formfield_data_%s" % count)
            for key, value in formfield_data.items():
                formfield = getattr(self, "formfield_%s" % count)
                self.assertEqual(getattr(formfield, key), value)

class AdminTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.editor = get_user_model().objects.create(
            username="editor",
            email="editor@test.com",
            is_superuser=True,
            is_staff=True
        )
        self.editor.set_password("password")
        self.editor.save()
        self.client.login(username="editor", password="password")

    def test_admin(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        load_fixtures(self)

    def test_detail(self):
        pass

    def test_list(self):
        pass

    def tearDown(self):
        pass
