import re
from htmlnode import *

from block_types import BlockType
from htmlnode import ParentNode
from textnode import TextType, TextNode

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text, {})
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

def text_to_children(text):
    nodes = [TextNode(text, TextType.TEXT)]
    
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return [text_node_to_html_node(node) for node in nodes]

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    matches_text = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches_text

def extract_markdown_links(text):
    matches_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches_links

def markdown_to_blocks(markdown):
    block_list = markdown.split("\n\n")

    new_block_list = []
    for block in block_list:
        stripped_block = block.strip()
        if stripped_block != "":
            new_block_list.append(stripped_block)

    return new_block_list

def block_to_block_type(markdown):    
    # HEADING CHECK
    hash_count = 0
    for char in markdown:
        
        if char == "#":
            hash_count += 1
        else:
            break

    if 1 <= hash_count <= 6 and len(markdown) > hash_count and markdown[hash_count] == ' ':
        return BlockType.HEADING

    # CODE CHECK
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE

    # QUOTE CHECK
    markdown_lines = markdown.split("\n")
    if all(line.startswith(">") for line in markdown_lines):
        return BlockType.QUOTE
    
    # UNORDERED LIST CHECK
    if all(line.startswith("* ") or line.startswith("- ") for line in markdown_lines):
        return BlockType.UNORDERED_LIST
    
    # ORDERED LIST CHECK
    if all(line.startswith(f"{i+1}. ") for i, line in enumerate(markdown_lines)):
        return BlockType.ORDERED_LIST
    
    # PARAGRAPHS
    else:
        return BlockType.PARAGRAPH
    
def parse_heading_block(block):
    hash_count = 0
    for char in block:
        if char == '#':
            hash_count += 1
        else:
            break
    
    content = block[hash_count:].strip()
    return hash_count, content

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    print("Blocks:", markdown_blocks)
    parent_node = ParentNode("div", [])
    
    for block in markdown_blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            paragraph_node = ParentNode("p", children=text_to_children(block))
            parent_node.add_child(paragraph_node)

        elif block_type == BlockType.HEADING:
            hash_count, content = parse_heading_block(block)
            heading_node = ParentNode(f"h{hash_count}", children=text_to_children(content))
            parent_node.add_child(heading_node)

        elif block_type == BlockType.CODE:
            content = block.strip()[3:-3].strip()

            code_node = ParentNode("code", children=text_to_children(content))
            pre_node = ParentNode("pre", children=[code_node])
            parent_node.add_child(pre_node)

        elif block_type == BlockType.QUOTE:
            content = block[1:].strip()
            quote_node = ParentNode("blockquote", children=text_to_children(content))
            parent_node.add_child(quote_node)

        elif block_type == BlockType.UNORDERED_LIST:
            items = block.split("\n")
            list_items = []

            for item in items:
                content = item[2:].strip()
                li_node = ParentNode("li", children=text_to_children(content))
                list_items.append(li_node)

            ul_node = ParentNode("ul", children=list_items)
            parent_node.add_child(ul_node)

        elif block_type == BlockType.ORDERED_LIST:
            items = block.split("\n")
            list_items = []

            for item in items:
                content = item[item.find(".")+1:].strip()
                li_node = ParentNode("li", children=text_to_children(content))
                list_items.append(li_node)

            ol_node = ParentNode("ol", children=list_items)
            parent_node.add_child(ol_node)    

    return parent_node
