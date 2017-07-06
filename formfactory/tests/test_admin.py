from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client

from formfactory.tests.test_base import load_fixtures


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

    def test_admin_action(self):
        response = self.client.get("/admin/formfactory/action/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/admin/formfactory/action/add/")
        self.assertEqual(response.status_code, 200)

        # Ensure that the action choice field is populated
        self.assertContains(response, self.action_data["action"])
        self.assertContains(response, self.dummy_action)

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

    def test_admin_fieldgroup(self):
        response = self.client.get("/admin/formfactory/formfieldgroup/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/admin/formfactory/formfieldgroup/add/")
        self.assertEqual(response.status_code, 200)

    def test_admin_field(self):
        response = self.client.get("/admin/formfactory/formfield/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/admin/formfactory/formfield/add/")
        self.assertEqual(response.status_code, 200)

    def test_admin_wizard(self):
        response = self.client.get("/admin/formfactory/wizard/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/admin/formfactory/wizard/add/")
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass
