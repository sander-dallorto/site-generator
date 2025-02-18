import re

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
    pass
            
    

   

