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

    kls.action_data = {
        "action": "formfactory.actions.store_data"
    }
    kls.action = models.Action.objects.create(**kls.action_data)

    kls.formactionthrough_data = {
        "action": kls.action,
        "form": kls.simpleform,
        "order": 0
    }
    kls.formactionthrough = models.FormActionThrough.objects.create(
        **kls.formactionthrough_data
    )

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


class ValidatorTestCase(TestCase):
    def setUp(self):
        self.validator = "formfactory.tests.formfactoryapp.validators.dummy_validator"

    def test_registry(self):
        self.assertIn(self.validator, validators.get_registered_validators())

    def test_unregistry(self):
        validator = validators.get_registered_validators()[self.validator]
        validators.unregister(validator)
        self.assertNotIn(
            self.validator, validators.get_registered_validators()
        )

    def test_action(self):
        validator = validators.get_registered_validators()[self.validator]
        self.assertTrue(validator(2))


class ActionTestCase(TestCase):
    def setUp(self):
        self.action = "formfactory.tests.formfactoryapp.actions.dummy_action"

    def test_registry(self):
        self.assertIn(self.action, actions.get_registered_actions())

    def test_unregistry(self):
        action = actions.get_registered_actions()[self.action]
        actions.unregister(action)
        self.assertNotIn(
            self.action, actions.get_registered_actions()
        )

    def test_action(self):
        action = actions.get_registered_actions()[self.action]
        self.assertTrue(action({}))


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
        response = self.client.get("/admin/formfactory/form/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/admin/formfactory/form/add/")
        self.assertEqual(response.status_code, 200)

    def test_admin_fieldoption(self):
        response = self.client.get("/admin/formfactory/fieldchoice/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/admin/formfactory/fieldchoice/add/")
        self.assertEqual(response.status_code, 200)

    def test_admin_formdata(self):
        response = self.client.get("/admin/formfactory/formdata/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/admin/formfactory/formdata/add/")
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

        form_data = {
            "uuid": form_factory.fields["uuid"].initial,
            "form_id": form_factory.fields["form_id"].initial,
            "name": "Name Surname",
            "email-address": "test@test.com",
            "accept-terms": True
        }
        form_factory = self.simpleform.as_form(data=form_data)

        self.assertTrue(form_factory.is_bound)
        self.assertFalse(bool(form_factory.errors))
        self.assertTrue(form_factory.is_valid())

    def test_save(self):
        form_factory = self.simpleform.as_form()
        form_data = {
            "uuid": form_factory.fields["uuid"].initial,
            "form_id": form_factory.fields["form_id"].initial,
            "name": "Name Surname",
            "email-address": "test@test.com",
            "accept-terms": True
        }
        form_factory = self.simpleform.as_form(data=form_data)
        self.assertTrue(form_factory.is_valid())

        form_factory.save()
        uuid = form_factory.fields["uuid"].initial
        form_store = models.FormData.objects.get(uuid=uuid)
        for field in form_store.items.all():
            self.assertEqual(
                field.value, str(form_data[field.form_field.slug])
            )

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
