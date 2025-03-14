import unittest

from text_processing import *
from textnode import TextNode, TextType

class TestSplitDelimiter(unittest.TestCase):
    def test_simple_case(self):
        node = TextNode("This is `code`", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            nodes, 
            [
            TextNode("This is ", TextType.TEXT),  
            TextNode("code", TextType.CODE)
            ]
            )
        
    def test_multiple_delimiters(self):
        node = TextNode("`Some` code `here and more` code `elsewhere`", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertNotEqual(
            nodes,
            [
                TextNode("Some", TextType.CODE),
                TextNode("code", TextType.TEXT),
                TextNode("here and more", TextType.CODE),
                TextNode("code", TextType.TEXT),
                TextNode("elsewhere", TextType.CODE)
            ]
        )

    def test_split_nodes_image(self):
        # Test case 1: No images
        node = TextNode("Just plain text", TextType.TEXT)
        nodes = split_nodes_image([node])
        assert len(nodes) == 1
        assert nodes[0].text == "Just plain text"
    
        # Test case 2: One image
        node = TextNode("Start ![image](https://example.com/img.png) end", TextType.TEXT)
        nodes = split_nodes_image([node])
        assert len(nodes) == 3
        assert nodes[0].text == "Start "
        assert nodes[1].text == "image"
        assert nodes[1].text_type == TextType.IMAGE
        assert nodes[1].url == "https://example.com/img.png"
        assert nodes[2].text == " end"

    def test_split_nodes_link(self):
        # Test case 1: No links
        node = TextNode("Plain text only", TextType.TEXT)
        nodes = split_nodes_link([node])
        assert len(nodes) == 1
        assert nodes[0].text == "Plain text only"
        
        # Test case 2: One link
        node = TextNode("Click [here](https://boot.dev) for more", TextType.TEXT)
        nodes = split_nodes_link([node])
        assert len(nodes) == 3
        assert nodes[0].text == "Click "
        assert nodes[1].text == "here"
        assert nodes[1].text_type == TextType.LINK
        assert nodes[1].url == "https://boot.dev"
        assert nodes[2].text == " for more"

    def test_text_to_textnodes_with_bold(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 3
        assert nodes[0].text == "This is "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "bold"
        assert nodes[1].text_type == TextType.BOLD
        assert nodes[2].text == " text"
        assert nodes[2].text_type == TextType.TEXT

    def test_text_to_textnodes_complex(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 10
        assert nodes[0].text == "This is "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "text"
        assert nodes[1].text_type == TextType.BOLD

if __name__ == "__main__":
    unittest.main()