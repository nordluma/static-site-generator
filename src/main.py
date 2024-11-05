from textnode import NodeType, TextNode


def main():
    node = TextNode("This is a text node", NodeType.BOLD, "https://boot.dev")
    print(node)


if __name__ == "__main__":
    main()
