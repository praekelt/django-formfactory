from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from formfactory.tests.test_base import load_fixtures


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        load_fixtures(self)

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

    def tearDown(self):
        pass
