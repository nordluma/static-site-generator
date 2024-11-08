from htmlnode import LeafNode, ParentNode
from textnode import TextType, TextNode


def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
    print(node)

    parent_node = ParentNode(
        tag="p",
        children=[
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )

    print(parent_node.to_html())
    print("----")

    leaf_node = LeafNode(
        tag="a", value="take action", props={"href": "not.phishing.com"}
    )
    print(leaf_node.props_to_html())


if __name__ == "__main__":
    main()
