from textnode import *

def main():
    node_object = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(node_object)
    
if __name__ == "__main__":
    main()