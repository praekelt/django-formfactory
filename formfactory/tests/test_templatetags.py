from django.template import Context, Template
from django.test import TestCase

from formfactory.tests.test_base import load_fixtures


class TemplateTagsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        load_fixtures(cls)

    def test_get_form_from_context(self):
        template = Template(
            "{% load formfactory_tags %}{% render_form form_object %}"
        )
        context = Context({"form_object": self.loginform})
        result = template.render(context)
        self.failUnless("login-form-form_id" in result)

    def test_get_form_by_slug(self):
        template = Template(
            "{% load formfactory_tags %}{% render_form 'login-form' %}"
        )
        result = template.render(Context())
        self.failUnless("login-form-form_id" in result)
