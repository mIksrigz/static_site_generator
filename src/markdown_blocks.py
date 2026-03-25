def markdown_to_blocks(markdown):
    markdown_blocks = markdown.split("\n\n")
    clean_markdown_blocks = []
    for block in markdown_blocks:
        clean_block = block.strip()
        if clean_block != "":
            clean_markdown_blocks.append(clean_block)
    return clean_markdown_blocks

