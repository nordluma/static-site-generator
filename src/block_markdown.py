import re

from htmlnode import HtmlNode, LeafNode, ParentNode
from markdown import text_to_textnodes
from textnode import text_node_to_html_node


def markdown_to_html_node(markdown_doc: str) -> HtmlNode:
    children = [block_to_html_node(block) for block in markdown_to_blocks(markdown_doc)]

    return ParentNode("div", children, None)


def block_to_html_node(block: str):
    block_type = block_to_block_type(block)
    if block_type == "heading":
        return heading_to_html_node(block)
    if block_type == "code":
        return code_to_html_node(block)
    if block_type == "quote":
        return quote_to_html_node(block)
    if block_type == "ordered_list":
        return olist_to_html_node(block)
    if block_type == "unordered_list":
        return ulist_to_html_node(block)
    if block_type == "paragraph":
        return paragraph_to_html_node(block)
    raise ValueError("Invalid block type")


def text_to_children(text: str) -> list[LeafNode]:
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def heading_to_html_node(block: str) -> ParentNode:
    lvl = block.count("#")
    if lvl + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {lvl}")
    # trim hashes and trailing space
    children = text_to_children(block[lvl + 1 :])

    return ParentNode(f"h{lvl}", children)


def quote_to_html_node(block: str) -> ParentNode:
    new_lines = []
    for line in block.splitlines():
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    children = text_to_children(" ".join(new_lines))
    return ParentNode("blockquote", children)


def code_to_html_node(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    # trim backticks from start and end
    children = text_to_children(block[4:-3])
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def paragraph_to_html_node(block: str) -> HtmlNode:
    paragraph = " ".join(block.splitlines())
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def ulist_to_html_node(block: str) -> ParentNode:
    return split_list_items(block, "ul", 2)


def olist_to_html_node(block: str) -> ParentNode:
    return split_list_items(block, "ol", 3)


def split_list_items(block: str, tag: str, prefix_len: int) -> ParentNode:
    html_items = []
    for item in block.splitlines():
        children = text_to_children(item[prefix_len:])
        html_items.append(ParentNode("li", children))
    return ParentNode(tag, html_items)


def block_to_block_type(block: str):
    if re.match(r"^#{1,6}", block):
        return "heading"
    elif block.startswith("```") and block.endswith("```"):
        return "code"
    elif is_quote_block(block):
        return "quote"
    elif is_unordered_list(block):
        return "unordered_list"
    elif is_ordered_list(block):
        return "ordered_list"

    return "paragraph"


def is_quote_block(block: str) -> bool:
    lines = block.split("\n")
    for line in lines:
        if not re.match(r"^>.*", line):
            return False
    return True


def is_unordered_list(block: str) -> bool:
    lines = block.split("\n")
    for line in lines:
        if not re.match(r"^[*-] .+", line):
            return False
    return True


def is_ordered_list(block: str) -> bool:
    lines = block.split("\n")
    for i, line in enumerate(lines, start=1):
        if not re.match(rf"^{i}\. .+", line):
            return False
    return True


def markdown_to_blocks(text: str) -> list[str]:
    blocks = text.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if not (block := block.strip()):
            continue
        filtered_blocks.append(block)

    return filtered_blocks
