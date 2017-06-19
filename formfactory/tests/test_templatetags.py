from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.test import LiveServerTestCase, Client
from django.test import TestCase

from formfactory.tests.test_base import load_fixtures


class TemplateTagsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        load_fixtures(cls)
        cls.client = Client()
        super(TemplateTagsTestCase, cls).setUpTestData()

    def test_get_form_by_slug(self):
        response = self.client.get(
            reverse(
                "render_tag"
            )
        )
        self.failUnless("login-form-form_id" in response.content)

    def test_default_detail_template(self):
        # Detail view already makes use of the render_form tag and passes an
        # object.
        response = self.client.get(
            reverse(
                "formfactory:form-detail",
                kwargs={"slug": "login-form"}
            )
        )
        self.failUnless("login-form-form_id" in response.content)
