import unittest

from markdown_utils import *
from block_types import BlockType

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

    def test_block_to_block_types(self):
        #Testing headers
        assert block_to_block_type("# Heading 1") == BlockType.HEADING
        assert block_to_block_type("### Heading 3") == BlockType.HEADING
        assert block_to_block_type("###### Heading 6") == BlockType.HEADING
        assert block_to_block_type("####### Too many '#'s'") == BlockType.PARAGRAPH

        #Testing codes
        assert block_to_block_type("``` this is some code ```") == BlockType.CODE
        assert block_to_block_type("`` this is NOT some code ``") == BlockType.PARAGRAPH

        #Testing quotes
        assert block_to_block_type(">This is a single quote") == BlockType.QUOTE
        assert block_to_block_type(">These are\n>Multiple quotes") == BlockType.QUOTE

        #Testing unordered lists
        assert block_to_block_type("* First item") == BlockType.UNORDERED_LIST
        assert block_to_block_type("- First item\n- Second item") == BlockType.UNORDERED_LIST

        # Test ordered lists
        assert block_to_block_type("1. First item\n2. Second item") == BlockType.ORDERED_LIST
    
        # Test paragraphs
        assert block_to_block_type("Just a normal paragraph") == BlockType.PARAGRAPH




if __name__ == "__main__":
    unittest.main()