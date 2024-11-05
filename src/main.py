from htmlnode import LeafNode
from textnode import TextType, TextNode


def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
    print(node)

    leaf_node = LeafNode("h1", "hello world")
    print(leaf_node)
    print(leaf_node.to_html())


if __name__ == "__main__":
    main()
