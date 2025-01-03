import re


def block_to_block_type(block: str):
    if re.match(r"^#{1,6}", block):  # heading
        return "heading"
    elif block.startswith("```") and block.endswith("```"):  # code
        return "code"
    elif is_quote_block(block):  # quote
        return "quote"
    elif is_unordered_list(block):  # unordered list
        return "unordered_list"
    elif is_ordered_list(block):  # ordered list
        return "ordered_list"

    return "paragraph"  # paragraph


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
