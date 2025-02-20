import unittest

from main import *

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# This is a title"
        self.assertEqual(extract_title(markdown), "This is a title")

    def test_extract_title_no_title(self):
        with self.assertRaises(ValueError):
            extract_title("This is not a title")

if __name__ == "__main__":
    unittest.main()