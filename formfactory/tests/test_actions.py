from django.test import TestCase

from formfactory import actions, exceptions
from formfactory.tests.test_base import load_fixtures


class DummyForm(object):
    def __init__(self, *args, **kwargs):
        self.cleaned_data = {}


class ActionTestCase(TestCase):
    def setUp(self):
        load_fixtures(self)
        self.dummy_form_instance = DummyForm()

    def test_registry(self):
        self.assertIn(self.dummy_action, actions.get_registered_actions())

    def test_unregistry(self):
        action = actions.get_registered_actions()[self.dummy_action]
        actions.unregister(action)
        self.assertNotIn(
            self.dummy_action, actions.get_registered_actions()
        )

    def test_action(self):
        action = actions.get_registered_actions()[self.dummy_action]
        self.assertTrue(action({}))

    def test_action_exception(self):
        self.assertRaises(
            exceptions.MissingActionParam,
            actions.send_email,
            form_instance=self.dummy_form_instance
        )
