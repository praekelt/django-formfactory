from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from formfactory import models


def load_fixtures(kls):
    pass


class ModelTestCase(TestCase):
    def setUp(self):
        load_fixtures(self)


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
