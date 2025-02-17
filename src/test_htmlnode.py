import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        actual_node_html = HTMLNode(props={" href": "https://google.com"})
        test_node_html = HTMLNode(props={"href": "https://www.google.com"})
        self.assertNotEqual(actual_node_html, test_node_html)

    def test_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    
    def test_one_prop(self):
        node = HTMLNode(props={"href": "https://google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com"')
    
class TestLeafNode(unittest.TestCase):
    def test_create_leaf_node(self):
        node = LeafNode("p", "Hello, World!")
        self.assertEqual(node.to_html(), "<p>Hello, World!</p>")

    def test_create_leaf_node_with_no_tag(self):
        node = LeafNode(None, "Hello, World!")
        self.assertEqual(node.to_html(), "Hello, World!")

    def test_create_leaf_node_with_props(self):
        node = LeafNode("a", "Hello, World!", {"href": "https://google.com"})
        self.assertEqual(node.to_html(), '<a href="https://google.com">Hello, World!</a>')
        
    def test_value_none(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)
        
        with self.assertRaises(ValueError):
            LeafNode("", "some text")

class TestParentNode(unittest.TestCase):
    #ParentNode takes (tag, children, props)
    def test_parent_with_props(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "Hello"),
                LeafNode("p", "World")
            ]
        )
        self.assertEqual(node.to_html(), "<div><p>Hello</p><p>World</p></div>")

    def test_nested_parent_nodes(self):
        nested_node = ParentNode(
        "div",
        [
            ParentNode(
                "p",
                [LeafNode("b", "Bold text")]
            )
        ]
    )
        self.assertEqual(nested_node.to_html(), "<div><p><b>Bold text</b></p></div>")  

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