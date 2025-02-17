import unittest

from markdown_utils import extract_markdown_links, extract_markdown_images

class TestMarkdownUtils(unittest.TestCase):
    def test_eq_link(self):
        test_text = extract_markdown_links("Here's an image ![example](https://example.com/image.png) and a link [to Boot.dev](https://www.boot.dev)")
        self.assertEqual([('to Boot.dev', 'https://www.boot.dev')], test_text)

    def test_eq_image(self):
        test_text = extract_markdown_images("Here's an image ![example](https://example.com/image.png) and a link [to Boot.dev](https://www.boot.dev)")
        self.assertEqual([("example", "https://example.com/image.png")], test_text)

if __name__ == "__main__":
    unittest.main()