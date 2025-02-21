import os
import shutil 
from textnode import *
from text_processing import *
from htmlnode import *

def main():
    node_object = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    copy_static_files(src="static", dest="public")

    if os.path.exists("public"):
        shutil.rmtree("public")

    shutil.copytree("static", "public")

    generate_page("content/index.md", "template.html", "public/index.html")

    print(node_object)
    
def copy_static_files(src="static", dest="public"):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

    def recursive_copy(src, dest):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dest, item)
            if os.path.isdir(s):
                os.mkdir(d)
                recursive_copy(s, d)
            else:
                print(f"Copying {s} to {d}")
                shutil.copy2(s, d)

    recursive_copy(src, dest)

def extract_title(markdown):
    splitted_markdown = markdown.split("\n")
    
    for line in splitted_markdown:
        if line.startswith("#"):
            return line[1:].strip()
    else:
        raise ValueError("No title found in the markdown input")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        content = f.read()
    print(f"Content length: {len(content)}")

    with open(template_path, "r") as f:
        template = f.read()
    print(f"Template length: {len(template)}")

    html_node = markdown_to_html_node(content)
    html_content = html_node.to_html()

    page_title = extract_title(content)

    template = template.replace("{{ Title }}", page_title)
    template = template.replace("{{ Content }}", html_content)

    directory = os.path.dirname(dest_path)
    os.makedirs(directory, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    entries = os.listdir(dir_path_content)

    for entry in entries:
        full_path = os.path.join(dir_path_content, entry)
        
        if os.path.isfile(full_path):
            if entry.endswith(".md"):
                relative_path = full_path[len(dir_path_content)+1:]
                modified_relative_path = relative_path.replace(".md", ".html")
                modified_dest_dir = os.path.join(dest_dir_path, modified_relative_path)

                generate_page(full_path, template_path, modified_dest_dir)

        else:
            new_dest = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(full_path, template_path, new_dest)






if __name__ == "__main__":
    main()