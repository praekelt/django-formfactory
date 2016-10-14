from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from formfactory import models
from formfactory.tests.test_base import load_fixtures


class ViewTestCase(TestCase):
    def setUp(self):
        load_fixtures(self)
        self.client = Client()
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

        self.user = User.objects.create(
            username="testuser", password="testpass"
        )
        self.loginform_factory = self.loginform.as_form()
        self.loginform_fields = self.loginform_factory.fields
        self.loginform_data = {
            "login-form-uuid": self.form_fields["uuid"].initial,
            "login-form-form_id": self.form_fields["form_id"].initial,
            "login-form-username": self.user.username,
            "login-form-password": self.user.password
        }

    def test_detail(self):
        response = self.client.get(
            reverse(
                "formfactory:form-detail",
                kwargs={"slug": self.simpleform_data["slug"]}
            )
        )
        self.assertEqual(response.status_code, 200)
        for field in self.simpleform.fields.all():
            self.assertContains(response, field.label)
            for choice in field.choices.all():
                self.assertContains(response, choice.label)
                self.assertContains(response, choice.value)

        response = self.client.post(
            reverse(
                "formfactory:form-detail",
                kwargs={"slug": self.simpleform_data["slug"]}
            ),
            data=self.form_data, follow=True
        )
        original_form_field = response.context["form"].fields
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Success")
        self.assertNotContains(response, "Failure")
        self.assertNotContains(response, "This field is required.")

        form_store = models.FormData.objects.get(
            uuid=original_form_field["uuid"].initial
        )
        for field in form_store.items.all():
            field_key = "%s-%s" % (
                self.form_factory.prefix, field.form_field.slug
            )
            self.assertEqual(field.value, str(self.form_data[field_key]))

    def test_login_detail(self):
        response = self.client.get(
            reverse(
                "formfactory:form-detail",
                kwargs={"slug": self.loginform_data["slug"]}
            )
        )
        self.assertEqual(response.status_code, 200)
        for field in self.loginform.fields.all():
            self.assertContains(response, field.label)

        response = self.client.post(
            reverse(
                "formfactory:form-detail",
                kwargs={"slug": self.loginform_data["slug"]}
            ),
            data=self.form_data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Success")
        self.assertNotContains(response, "Failure")
        self.assertNotContains(response, "This field is required.")
        self.assertTrue(self.user.is_autheticated())

    def tearDown(self):
        pass
