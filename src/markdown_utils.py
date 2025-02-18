import re
from block_types import BlockType

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