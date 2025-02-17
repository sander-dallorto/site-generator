import re

def extract_markdown_images(text):
    matches_text = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches_text

def extract_markdown_links(text):
    matches_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches_links
