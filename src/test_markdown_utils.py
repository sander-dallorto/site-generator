import unittest

from text_processing import *
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

    def test_markdown_to_html_node(self):
        # Test paragraph
        print("Actual output:", markdown_to_html_node("This is a paragraph").to_html())
        assert markdown_to_html_node("This is a paragraph").to_html() == "<div><p>This is a paragraph</p></div>"
        
        # Test heading
        assert markdown_to_html_node("# Heading").to_html() == "<div><h1>Heading</h1></div>"
        
        # Test code block
        assert markdown_to_html_node("```\ncode block\n```").to_html() == "<div><pre><code>code block</code></pre></div>"
        
        # Test blockquote
        assert markdown_to_html_node("> quote").to_html() == "<div><blockquote>quote</blockquote></div>"
        
        # Test unordered list
        assert markdown_to_html_node("- item 1\n- item 2").to_html() == "<div><ul><li>item 1</li><li>item 2</li></ul></div>"
        
        # Test ordered list
        assert markdown_to_html_node("1. item 1\n2. item 2").to_html() == "<div><ol><li>item 1</li><li>item 2</li></ol></div>"


if __name__ == "__main__":
    unittest.main()