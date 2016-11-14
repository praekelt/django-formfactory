from django.test import TestCase

from formfactory import models, utils


class UtilsTestCase(TestCase):
    def setUp(self):
        pass

    def test_get_all_model_fields(self):
        self.assertEqual(
            utils.get_all_model_fields(models.FormData),
            ["items", "id", "uuid", "form"]
        )

    def tearDown(self):
        pass
