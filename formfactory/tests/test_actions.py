from django.test import TestCase

from formfactory import actions
from formfactory.tests.test_base import load_fixtures


class ActionTestCase(TestCase):
    def setUp(self):
        load_fixtures(self)

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
