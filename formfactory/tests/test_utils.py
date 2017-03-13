import os

from django.test import TestCase

from formfactory import models, utils


class UtilsTestCase(TestCase):
    def setUp(self):
        self.file_path = "/tmp/test.txt"

    def test_get_all_model_fields(self):
        self.assertEqual(
            utils.get_all_model_fields(models.FormData),
            ["items", "id", "uuid", "form"]
        )

    def test_set_file_name(self):
        self.assertEqual(
            utils.set_file_name(self.file_path, count=0), self.file_path
        )
        self.assertEqual(
            utils.set_file_name(self.file_path, count=1), "/tmp/test_1.txt"
        )

    def test_increment_file_name(self):
        self.assertEqual(
            utils.increment_file_name(self.file_path), self.file_path
        )

        file_buffer = open(self.file_path, "wb+")
        file_buffer.write("Test")
        file_buffer.close()
        self.assertEqual(
            utils.increment_file_name(self.file_path), "/tmp/test_1.txt"
        )

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
