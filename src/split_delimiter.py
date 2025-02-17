from htmlnode import *
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            text = old_node.text
            first_delimiter = text.find(delimiter)
            second_delimiter = text.find(delimiter, first_delimiter + 1)

            if first_delimiter == -1 or second_delimiter == -1:
                raise Exception("Delimiters don't match")
            
            if first_delimiter != -1 and second_delimiter != -1:
                before = text[:first_delimiter]
                between = text[first_delimiter + 1:second_delimiter]
                after = text[second_delimiter + 1:]

                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
                if between:
                    new_nodes.append(TextNode(between, text_type))
                if after:
                    new_nodes.append(TextNode(after, TextType.TEXT))

            else:
                new_nodes.append(old_node)
            
    return new_nodes

if __name__ == "__main__":
    node = TextNode("Hello `world` today", TextType.TEXT)
    nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    
    for node in nodes:
        print(f"Text: '{node.text}', Type: {node.text_type}")