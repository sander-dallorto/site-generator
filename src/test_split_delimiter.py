import unittest

from split_delimiter import split_nodes_delimiter
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
        
    # THIS SHOULD FAIL WITH CURRENT IMPLEMENTATION
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

    def test_unmatched_delimiters(self):
        node = TextNode("This is a **mismatched` delimiter example", TextType.TEXT)
        
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertTrue("Delimiters don't match" in str(context.exception))

if __name__ == "__main__":
    unittest.main()