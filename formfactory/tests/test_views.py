from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
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
        self.form_postdata = {
            "subscribe-form-uuid": self.form_fields["uuid"].initial,
            "subscribe-form-form_id": self.form_fields["form_id"].initial,
            "subscribe-form-salutation": "Mr",
            "subscribe-form-name": "Name Surname",
            "subscribe-form-email-address": "test@test.com",
            "subscribe-form-accept-terms": True,
            "subscribe-form-to-email": "dev@praekelt.com",
            "subscribe-form-subject": "Test Email"
        }

        self.user = get_user_model().objects.create(username="testuser")
        self.user.set_password("testpass")
        self.user.save()

        self.loginform_factory = self.loginform.as_form()
        self.loginform_fields = self.loginform_factory.fields
        self.loginform_postdata = {
            "login-form-uuid": self.form_fields["uuid"].initial,
            "login-form-form_id": self.form_fields["form_id"].initial,
            "login-form-username": "testuser",
            "login-form-password": "testpass"
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
            data=self.form_postdata, follow=True
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
            self.assertEqual(field.value, str(self.form_postdata[field_key]))

    def tearDown(self):
        pass


class LoginViewDetailTestCase(TestCase):
    def setUp(self):
        super(LoginViewDetailTestCase, self).setUp()
        load_fixtures(self)
        self.form_factory = self.simpleform.as_form()
        self.form_fields = self.form_factory.fields
        self.loginform_postdata = {
            "login-form-uuid": self.form_fields["uuid"].initial,
            "login-form-form_id": self.form_fields["form_id"].initial,
            "login-form-username": "testuser",
            "login-form-password": "testpass"
        }

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
            data=self.loginform_postdata, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Success")
        self.assertNotContains(response, "Failure")
        self.assertNotContains(response, "This field is required.")


class WizardViewTestCase(TestCase):
    def setUp(self):
        super(WizardViewTestCase, self).setUp()
        load_fixtures(self)

        # create wizard object
        wizard_data = {
            "title": "Test wizard",
            "slug": "test-wizard",
            "success_message": "Success",
            "failure_message": "Failure"
        }
        self.wizard = models.Wizard.objects.create(**wizard_data)

        # add forms to the wizard
        models.FormOrderThrough.objects.create(
            wizard=self.wizard, form=self.simpleform, order=0
        )
        models.FormOrderThrough.objects.create(
            wizard=self.wizard, form=self.loginform, order=1
        )

    def post_simple_form_step(self):
        simple_form_uuid_field = self.simpleform.as_form().fields["uuid"].initial
        post_data = {
            "FactoryWizardView-test-wizard-current_step": "subscribe-form",
            "subscribe-form-salutation": "Mr",
            "subscribe-form-name": "Tester",
            "subscribe-form-email-address": "tester@example.com",
            "subscribe-form-accept_terms": True,
            "subscribe-form-to-email": "dev@example.com",
            "subscribe-form-subject": "Test email",
            "subscribe-form-form_id": self.simpleform.id,
            "subscribe-form-uuid": simple_form_uuid_field,
        }
        response = self.client.post(
            reverse("formfactory:wizard-detail", kwargs={
                "slug": self.wizard.slug,
                "step": "subscribe-form"
            }),
            data=post_data,
            follow=True
        )
        return response

    def post_login_form_step(self):
        login_form_uuid_field = self.loginform.as_form().fields["uuid"].initial
        post_data = {
            "FactoryWizardView-test-wizard-current_step": "login-form",
            "login-form-username": "tester",
            "login-form-password": "0000",
            "login-form-form_id": self.loginform.id,
            "login-form-uuid": login_form_uuid_field,
        }
        response = self.client.post(
            reverse("formfactory:wizard-detail", kwargs={
                "slug": self.wizard.slug,
                "step": "login-form"
            }),
            data=post_data,
            follow=True
        )
        return response

    def test_wizard_detail(self):
        """Validate that the WizardView is instantiated correctly
        from the DB wizard object; and that the forms are rendered in the defined
        order.
        """
        response = self.client.get(
            reverse("formfactory:wizard-detail", kwargs={
                "slug": self.wizard.slug,
                "step": "subscribe-form"
            })
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.simpleform.id, response.context["form"].fields["form_id"].initial)

        # post first wizard step and redirect to second step
        response = self.post_simple_form_step()
        url, status_code = response.redirect_chain[-1]
        self.assertEqual("/formfactory/test-wizard/login-form/", url)

        # post second step and redirect to url specified for wizard object in DB
        self.post_login_form_step()
        # TODO

    # These tests exist because we overwrote existing functionality, and we
    # need to make sure that it stills works as expected
    def test_wizard_redirect_to_first_step(self):
        pass

    def test_redirect_to_url_specified_in_urls(self):
        pass

    # One way of performing per-form actions in the wizard is to step through the
    # wizard and call each form's save() method, because form actions are called there.
    # This could be achieved by having a wizard action that calls each form's save
