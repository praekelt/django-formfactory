from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound
from django.template import Context, Template, TemplateSyntaxError
from django.test import LiveServerTestCase, Client
from django.test import TestCase

from formfactory.tests.test_base import load_fixtures


class TemplateTagsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        load_fixtures(cls)
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

    def test_tag_syntax_error(self):
        with self.assertRaisesMessage(
            TemplateSyntaxError, "{% render_form <form_slug>/<object> %}"
        ):
            response = self.client.get(
                reverse(
                    "render_tag_syntax_error"
                )
            )

    def test_tag_raise_404(self):
        response = self.client.get(
            reverse(
                "render_tag_404"
            )
        )
        self.failUnless(response.status_code, 404)

    def test_all_fields_get_form_by_slug(self):
        response = self.client.get(
            reverse(
                "render_tag_all_fields"
            )
        )
        self.failUnless("subscribe-form" in response.content)
