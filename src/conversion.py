from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.NORMAL.value:
            node = LeafNode(None, text_node.text)
        case TextType.BOLD.value:
            node = LeafNode("b", text_node.text)
        case TextType.ITALIC.value:
            node = LeafNode("i", text_node.text)
        case TextType.CODE.value:
            node = LeafNode("code", text_node.text)
        case TextType.LINK.value:
            node = LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE.value:
            node = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("invalid text type for `TextNode`")
    return node
