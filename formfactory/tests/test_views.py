from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.http.request import HttpRequest
from django.test import TestCase
from django.test.client import Client

from formfactory import models
from formfactory.tests.test_base import cleanup_files, load_fixtures


class ViewTestCase(TestCase):
    def setUp(self):
        load_fixtures(self)
        cleanup_files()

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
            "subscribe-form-subject": "Test Email",
            "subscribe-form-upload-to": "uploads/test",
            "subscribe-form-id-copy": SimpleUploadedFile("test.txt", "Test")
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
        response = self.client.get(self.simpleform.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        for field_group in self.simpleform.fieldgroups.all():
            for field in field_group.fields.all():

                # Paragraph fields are never required.
                if field.slug == "paragraph":
                    continue
                self.assertContains(response, field.slug)
                for choice in field.choices.all():
                    self.assertContains(response, choice.label)
                    self.assertContains(response, choice.value)

        response = self.client.post(
            self.simpleform.get_absolute_url(),
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

    def test_formfield_group_title_can_be_hidden(self):
        response = self.client.get(
            self.simpleform.get_absolute_url()
        )
        self.assertEqual(response.status_code, 200)
        self.failIf("Field Group 1" in response.content)


class ViewNoCSRFTestCase(ViewTestCase):
    """Re-use the super class. It tests all the required code paths."""

    def setUp(self):
        super(ViewNoCSRFTestCase, self).setUp()

        # Explicitly enable CSRF checks to confirm the bypass works
        self.client = Client(enforce_csrf_checks=True)

        # Modify the form
        self.simpleform.enable_csrf = False
        self.simpleform.save()


class LoginViewDetailTestCase(TestCase):
    def setUp(self):
        load_fixtures(self)
        self.form_factory = self.simpleform.as_form()
        self.form_fields = self.form_factory.fields
        self.loginform_postdata = {
            "login-form-uuid": self.form_fields["uuid"].initial,
            "login-form-form_id": self.form_fields["form_id"].initial,
            "login-form-username": "testuser",
            "login-form-password": "testpass"
        }

    def test_detail(self):
        response = self.client.get(self.loginform.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        for field_group in self.loginform.fieldgroups.all():
            self.assertContains(response, field_group.title)
            for field in field_group.fields.all():
                self.assertContains(response, field.label)

        response = self.client.post(
            self.loginform.get_absolute_url(),
            data=self.loginform_postdata, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Success")
        self.assertNotContains(response, "Failure")
        self.assertNotContains(response, "This field is required.")

        # Ensure the correct template was used, in this case the login template
        # is overridden with formfactory/tests/templates/form_detail-login.html
        self.assertContains(response, "Login Templete Override")

        # Ensure the correct button text is rendered
        self.assertContains(
            response, self.loginform_data["submit_button_text"]
        )


class WizardViewTestCase(TestCase):
    def setUp(self):
        super(WizardViewTestCase, self).setUp()
        load_fixtures(self)

    def get_first_step(self):
        response = self.client.get(
            reverse("formfactory:wizard-detail", kwargs={
                "slug": self.wizard.slug,
                "step": "subscribe-form"
            })
        )
        return response

    def post_first_step(self):
        simple_form_uuid_field = \
            self.simpleform.as_form().fields["uuid"].initial
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
            "subscribe-form-upload-to": "uploads/test",
            "subscribe-form-id-copy": SimpleUploadedFile("test.txt", "Test")
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

    def post_second_step(self):
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

    def test_detail(self):
        """Validate that the WizardView is instantiated correctly
        from the DB wizard object; and that the forms are rendered in the
        defined order.
        """
        response = self.get_first_step()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.simpleform.id,
            response.context["form"].fields["form_id"].initial
        )

        # post first wizard step and redirect to second step
        response = self.post_first_step()
        url, status_code = response.redirect_chain[-1]
        self.assertEqual("/formfactory/wizard/test-wizard/login-form/", url)

        # post second step and redirect to url specified for wizard
        # object in DB
        response = self.post_second_step()
        url, status_code = response.redirect_chain[-1]
        self.assertEqual("/", url)

    def test_form_actions_at_done_step(self):
        """Verify that form actions are called on the wizard's done()
        step.
        Each form is saved in the wizard's done() step, and each form's
        save() method calls the form's actions.
        The `simpleform` form has two actions; `store_data` and `send_email`.
        """
        action_data = {
            "action": "formfactory.tests.actions.dummy_wizard_action"
        }
        action = models.Action.objects.create(**action_data)
        wizard_actionthrough_data = {
            "action": action,
            "wizard": self.wizard,
            "order": 0
        }
        models.WizardActionThrough.objects.create(**wizard_actionthrough_data)

        self.get_first_step()
        self.post_first_step()
        self.post_second_step()

        # validate `store_data` action was performed for `simpleform`
        form_data = models.FormData.objects.get(form_id=self.simpleform.id)

        self.assertTrue(models.FormDataItem.objects.filter(
            form_data=form_data, value="Mr").exists())
        self.assertTrue(models.FormDataItem.objects.filter(
            form_data=form_data, value="Tester").exists())
        self.assertTrue(models.FormDataItem.objects.filter(
            form_data=form_data, value="tester@example.com").exists())

    def tearDown(self):
        pass


class FormHasRequestObjectTestCase(TestCase):
    """Formfactory views should pass request to forms
    """

    @classmethod
    def setUpTestData(cls):
        load_fixtures(cls)

    def test_request_is_passed_to_forms(self):
        response = self.client.get(
            reverse("formfactory:form-detail", args=[self.simpleform.slug]),
        )
        self.assertTrue(
            isinstance(response.context["form"].request, HttpRequest)
        )
