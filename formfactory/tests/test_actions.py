from django.test import TestCase

from formfactory import actions


class ActionTestCase(TestCase):
    def setUp(self):
        self.action = "formfactory.tests.actions.dummy_action"

    def test_registry(self):
        self.assertIn(self.action, actions.get_registered_actions())

    def test_unregistry(self):
        action = actions.get_registered_actions()[self.action]
        actions.unregister(action)
        self.assertNotIn(
            self.action, actions.get_registered_actions()
        )

    def test_action(self):
        action = actions.get_registered_actions()[self.action]
        self.assertTrue(action({}))
