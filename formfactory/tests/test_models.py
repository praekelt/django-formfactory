from django import forms
from django.test import TestCase

from formfactory import models
from formfactory.tests.test_base import load_fixtures


class ModelTestCase(TestCase):
    def setUp(self):
        load_fixtures(self)

    def test_field_constant(self):
        self.assertIn(("django.forms.fields.DateTimeField", "DateTimeField"), models.FIELD_TYPES)
        self.assertIn(("django.forms.fields.BooleanField", "BooleanField"), models.FIELD_TYPES)
        self.assertIn(("django.forms.fields.CharField", "CharField"), models.FIELD_TYPES)
        self.assertIn(("formfactory.fields.ParagraphField", "ParagraphField"), models.FIELD_TYPES)

        self.assertIn(("django.forms.widgets.TextInput", "TextInput"), models.WIDGET_TYPES)
        self.assertIn(("django.forms.widgets.DateTimeInput", "DateTimeInput"), models.WIDGET_TYPES)
        self.assertIn(("django.forms.widgets.CheckboxInput", "CheckboxInput"), models.WIDGET_TYPES)
        self.assertIn(("formfactory.widgets.ParagraphWidget", "ParagraphWidget"), models.WIDGET_TYPES)

        self.assertIn(
            self.action_data["action"], [a[0] for a in models.FORM_ACTIONS]
        )

        self.assertIn(
            self.dummy_validator,
            [v[0] for v in models.ADDITIONAL_VALIDATORS]
        )

    def test_form(self):
        for key, value in self.form_data.items():
            self.assertEqual(getattr(self.form, key), value)
        self.assertEqual(self.form.fieldgroups.count(), 1)
        self.assertIsInstance(self.form.as_form(), forms.Form)
        self.assertEqual(
            self.form.get_absolute_url(), "/formfactory/%s/" % self.form.slug
        )
        self.assertEqual(unicode(self.form), u"Form 1")

    def test_fieldchoice(self):
        for key, value in self.fieldchoice_data.items():
            self.assertEqual(getattr(self.fieldchoice, key), value)

    def test_modelchoices(self):
        for key, value in self.enumitem_data.items():
            self.assertEqual(getattr(self.enumitem, key), value)

    def test_formfield(self):
        for count in range(len(models.FIELD_TYPES)):
            formfield_data = getattr(self, "formfield_data_%s" % count)
            for key, value in formfield_data.items():
                formfield = getattr(self, "formfield_%s" % count)
                self.assertEqual(getattr(formfield, key), value)

    def test_formdata(self):
        for key, value in self.formdata_data.items():
            self.assertEqual(getattr(self.formdata, key), value)

    def test_formdataitem(self):
        for key, value in self.formdataitem_data.items():
            self.assertEqual(getattr(self.formdataitem, key), value)

    def test_fieldgroup(self):
        for key, value in self.fieldgroup_data.items():
            self.assertEqual(getattr(self.fieldgroup, key), value)

    def test_wizard(self):
        import django

        # This regression to django.db.sql.compiler.find_ordering_name() is
        # only present in these two django version.
        if django.get_version() in ["1.9", "1.9.1"]:
            forms = [instance.form for
                instance in models.WizardFormThrough.objects.filter(
                    wizard=self.wizard).order_by("order")
            ]
            self.assertQuerysetEqual(
                forms,
                [repr(self.simpleform), repr(self.loginform)]
            )
        else:
            self.assertQuerysetEqual(
                self.wizard.forms.all().order_by("wizardformthrough"),
                [repr(self.simpleform), repr(self.loginform)]
            )
        self.assertEqual(
            self.wizard.get_absolute_url(),
            "/formfactory/wizard/%s/" % self.wizard.slug
        )
