from enum import Enum

from htmlnode import LeafNode

type MaybeStr = str | None


class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: MaybeStr = None):
        self.text = text
        self.text_type = text_type.value
        self.url = url

    def __eq__(self, other) -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


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
