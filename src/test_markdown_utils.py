import unittest

from markdown_utils import extract_markdown_links, extract_markdown_images, markdown_to_blocks

class TestMarkdownUtils(unittest.TestCase):
    def test_eq_link(self):
        test_text = extract_markdown_links("Here's an image ![example](https://example.com/image.png) and a link [to Boot.dev](https://www.boot.dev)")
        self.assertEqual([('to Boot.dev', 'https://www.boot.dev')], test_text)

    def test_eq_image(self):
        test_text = extract_markdown_images("Here's an image ![example](https://example.com/image.png) and a link [to Boot.dev](https://www.boot.dev)")
        self.assertEqual([("example", "https://example.com/image.png")], test_text)

    def test_markdown_to_blocks(self):
        test_input = "Block 1\n\nBlock 2"
        expected = ["Block 1", "Block 2"]
        result = markdown_to_blocks(test_input)
        assert result == expected

    def test_markdown_to_blocks_extra(self):
        assert markdown_to_blocks("Block 1\n\nBlock 2") == ["Block 1", "Block 2"]
        assert markdown_to_blocks("  Block 1  \n\n  Block 2  ") == ["Block 1", "Block 2"]
        assert markdown_to_blocks("Block 1\n\n\n\nBlock 2") == ["Block 1", "Block 2"]
        assert markdown_to_blocks("Just one block") == ["Just one block"]

    def test_empty_block(self):
        assert markdown_to_blocks("") == []

    def test_white_spaces_only(self):
        assert markdown_to_blocks("  \n\n  \n\n   ") == []

if __name__ == "__main__":
    unittest.main()