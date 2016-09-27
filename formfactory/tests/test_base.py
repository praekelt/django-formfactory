from django import forms
from django.contrib.auth import get_user_model
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
            "slug": "form-field-%s" % count,
            "position": count,
            "form": kls.form,
            "field_type": field_type[0],
            "label": "Form Field %s" % count,
        })
        setattr(kls, "formfield_%s" % count, models.FormField.objects.create(
            **getattr(kls, "formfield_data_%s" % count)
        ))

    kls.simpleform_data = {
        "title": "Subscribe Form",
        "slug": "contact"
    }
    kls.simpleform = models.Form.objects.create(**kls.simpleform_data)

    kls.simpleformfield_data = {
        "name": {
            "title": "Name",
            "slug": "name",
            "position": 0,
            "form": kls.simpleform,
            "field_type": "CharField",
            "label": "Full Name",
            "required": False
        },
        "email_address": {
            "title": "Email Address",
            "slug": "email-address",
            "position": 1,
            "form": kls.simpleform,
            "field_type": "EmailField",
            "label": "Email",
            "help_text": "The email you would like info to be sent to"
        },
        "accept_terms": {
            "title": "Accept Terms",
            "slug": "accept-terms",
            "position": 2,
            "form": kls.simpleform,
            "field_type": "BooleanField",
            "label": "Do you accept the terms and conditions",
            "required": False
        }
    }
    for key, value in kls.simpleformfield_data.items():
        setattr(
            kls, "simpleformfield_%s" % key,
            models.FormField.objects.create(**value)
        )


class TestValidatorIncomplete(validators.BaseValidator):
    pass


class TestActionIncomplete(actions.BaseAction):
    pass


class TestValidator(validators.BaseValidator):
    validation_message = "%(value) is not divible by 2"

    def condition(self, value):
        return not value % 2


class TestAction(actions.BaseAction):
    def run(self, form_data):
        return True


class ValidatorTestCase(TestCase):
    def setUp(self):
        self.validator = TestValidator()
        self.incomplete_validator = TestValidatorIncomplete()

    def test_registry(self):
        validators.register(self.validator)
        self.assertIn(self.validator, validators.get_registered_validators())

    def test_unregistry(self):
        validators.register(self.validator)
        self.assertIn(self.validator, validators.get_registered_validators())

        validators.unregister(self.validator)
        self.assertNotIn(
            self.validator, validators.get_registered_validators()
        )

    def test_validation(self):

        # Ensure an excepetion is raised if the validation class is not
        # complete.
        self.assertRaises(
            NotImplementedError, self.incomplete_validator.validate, None
        )

        # Ensure that the validate method returns correctly
        self.assertTrue(self.validator.validate(4))


class ActionTestCase(TestCase):
    def setUp(self):
        self.action = TestAction()
        self.incomplete_action = TestActionIncomplete()

    def test_registry(self):
        actions.register(self.action)
        self.assertIn(self.action, actions.get_registered_actions())

    def test_unregistry(self):
        actions.register(self.action)
        self.assertIn(self.action, actions.get_registered_actions())

        actions.unregister(self.action)
        self.assertNotIn(self.action, actions.get_registered_actions())

    def test_action(self):

        # ensure an excpetion is raised if the validation class is not complete
        self.assertRaises(
            NotImplementedError, self.incomplete_action.run, None
        )

        # ensure that the run method returns correctly
        self.assertTrue(self.action.run({}))


class ModelTestCase(TestCase):
    def setUp(self):
        load_fixtures(self)

    def test_field_constant(self):
        self.assertIn(("DateTimeField", "DateTimeField"), models.FIELD_TYPES)
        self.assertIn(("BooleanField", "BooleanField"), models.FIELD_TYPES)
        self.assertIn(("CharField", "CharField"), models.FIELD_TYPES)

    def test_form(self):
        for key, value in self.form_data.items():
            self.assertEqual(getattr(self.form, key), value)
        self.assertEqual(self.form.fields.count(), len(models.FIELD_TYPES))
        self.assertIsInstance(self.form.as_form(), forms.Form)

    def test_formfield(self):
        for count in range(len(models.FIELD_TYPES)):
            formfield_data = getattr(self, "formfield_data_%s" % count)
            for key, value in formfield_data.items():
                formfield = getattr(self, "formfield_%s" % count)
                self.assertEqual(getattr(formfield, key), value)


class AdminTestCase(TestCase):
    def setUp(self):
        load_fixtures(self)
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

        response = self.client.get("/admin/formfactory/")
        self.assertEqual(response.status_code, 200)

    def test_admin_form(self):
        response = self.client.get("/admin/formfactory/form/add/")
        self.assertEqual(response.status_code, 200)

    def test_admin_fieldoption(self):
        response = self.client.get("/admin/formfactory/fieldchoice/add/")
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass


class FactoryTestCase(TestCase):
    def setUp(self):
        load_fixtures(self)

    def test_form(self):
        form_factory = self.simpleform.as_form()
        for value in self.simpleformfield_data.values():
            self.assertIn(value["slug"], [f for f in form_factory.fields])
            for k, v in value.items():
                if k in ["label", "help_text", "required"]:
                    self.assertEqual(
                        v, getattr(form_factory.fields[value["slug"]], k)
                    )

        form_factory = self.simpleform.as_form(data={
            "uuid": form_factory.fields["uuid"].initial,
            "name": "Name Surname",
            "email-address": "test@test.com",
            "accept-terms": True
        })

        self.assertTrue(form_factory.is_bound)
        self.assertFalse(bool(form_factory.errors))
        self.assertTrue(form_factory.is_valid())

    def tearDown(self):
        pass


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
