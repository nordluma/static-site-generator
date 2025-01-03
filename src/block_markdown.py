def markdown_to_blocks(text: str) -> list[str]:
    blocks = text.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if not (block := block.strip()):
            continue
        filtered_blocks.append(block)

    return filtered_blocks
