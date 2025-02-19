from textnode import *

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def add_child(self, child):
        self.children.append(child)
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props and len(self.props) > 0:
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



