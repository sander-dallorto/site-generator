import unittest

from textnode import TextNode, TextType
from text_processing import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a different text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_opt_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_diff_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        node2 = TextNode("This is a text node", TextType.ITALIC, "www.google.com")
        self.assertNotEqual(node, node2)

    def test_diff_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.bing.com")
        self.assertNotEqual(node, node2)

def test_text_node_to_html_node():
    # Test plain text
    text_node = TextNode("Hello, world!", TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    assert html_node.tag == ""
    assert html_node.value == "Hello, world!"
    assert html_node.props == {}

    # Test bold text
    text_node = TextNode("Bold text", TextType.BOLD)
    html_node = text_node_to_html_node(text_node)
    assert html_node.tag == "b"
    assert html_node.value == "Bold text"
    assert html_node.props == {}

    # Test link
    text_node = TextNode("Click me", TextType.LINK)
    text_node.url = "https://www.boot.dev"
    html_node = text_node_to_html_node(text_node)
    assert html_node.tag == "a"
    assert html_node.value == "Click me"
    assert html_node.props == {"href": "https://www.boot.dev"}

    # Test image
    text_node = TextNode("Alt text", TextType.IMAGE)
    text_node.url = "image.png"
    html_node = text_node_to_html_node(text_node)
    assert html_node.tag == "img"
    assert html_node.value == ""
    assert html_node.props == {"src": "image.png", "alt": "Alt text"}

if __name__ == "__main__":
    unittest.main()