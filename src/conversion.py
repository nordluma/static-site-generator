import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        # node has already a special text type, skip it
        if old_node.text_type != TextType.TEXT:
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
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for alt_text, image in images:
            sections = original_text.split(f"![{alt_text}]({image})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    alt_text,
                    TextType.IMAGE,
                    image,
                )
            )
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes
def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    # images = re.findall(r"\(![.*?]\)\((.*?)\)", text)
    images = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return [(alt_text, url) for alt_text, url in images]


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    links = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return [(alt_text, url) for alt_text, url in links]
