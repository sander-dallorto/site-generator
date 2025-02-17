from textnode import *

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props != None:
            props_line = " " + " ".join([f'{key}="{value}"' for key, value in self.props.items()])
            return props_line
        else:
            return ""
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("All leaf nodes must have a value")
        
        if tag == "":
            raise ValueError("Tag cannot be an empty string")
        
        super().__init__(tag, value, [], props)

    def to_html(self):
        if self.tag is None:
            return self.value
        
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"

        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, [], children, props)

    def to_html(self):
        if self.tag == "":
            raise ValueError("Tag cannot be an empty string")

        if self.children is None:
            raise ValueError("Must have a children node")
        
        if self.props is None:
            opening_tag = f"<{self.tag}>"
        
        else:
            opening_tag = f"<{self.tag}{self.props_to_html()}>"

        result = ""

        for child in self.children:
            result += child.to_html()

        return f"{opening_tag}{result}</{self.tag}>"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode("", text_node.text, {})
    elif text_node.text_type == TextType.BOLD:    
        return LeafNode("b", text_node.text, {})
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text, {})
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text, {})
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("Unknown text type")


