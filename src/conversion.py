import re

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


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        # node has already a special text type, skip it
        if old_node.text_type != TextType.NORMAL.value:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid Markdown. {text_type} section not closed")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            # When we split the text with the chosen delimiter the list is
            # always even if the markdown is valid (this is checked above).
            # This means that all elements with even index is "normal" text and
            # elements with odd index are the ones we are looking for.
            #
            # Example:
            #
            # Index                                 0             1           2
            # "This is a `code block` text" -> ["This is a", "code block", "text"]
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.NORMAL))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    # images = re.findall(r"\(![.*?]\)\((.*?)\)", text)
    images = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return [(alt_text, url) for alt_text, url in images]


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    links = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return [(alt_text, url) for alt_text, url in links]
