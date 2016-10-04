import unittest
from stitcher.configuration import NumField
from stitcher.configuration import FileField
from stitcher.configuration import DirectoryField

class TestField(unittest.TestCase):
    def setUp(self):
        num_field = NumField("numerical field", 0)
        self.num_field = num_field
        self.file_field = FileField("file field", "Makefile")
        self.dir_field = DirectoryField("directory field", "test/")

    def test_number_field_raises_exception_if_given_non_number(self):
        self.assertRaises(ValueError, self.num_field.update, "NAN")
        self.assertRaises(ValueError, self.num_field.update, "1")

    def test_file_field_raises_exception_if_given_non_file(self):
        self.assertRaises(ValueError, self.file_field.update, "non-existant-file")

    def test_directory_field_raises_exception_if_given_non_directory(self):
        self.assertRaises(ValueError, self.dir_field.update, "non-existant-directory/")
