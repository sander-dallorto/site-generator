import re

def extract_markdown_images(text):
    matches_text = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches_text

def extract_markdown_links(text):
    matches_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches_links

text = "Here's an image ![example](https://example.com/image.png) and a link [to Boot.dev](https://www.boot.dev)"
print(extract_markdown_images(text))
print(extract_markdown_links(text))