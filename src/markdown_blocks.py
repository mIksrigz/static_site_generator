import re
from enum import Enum


def markdown_to_blocks(markdown):
    markdown_blocks = markdown.split("\n\n")
    clean_markdown_blocks = []
    for block in markdown_blocks:
        clean_block = block.strip()
        if clean_block != "":
            clean_markdown_blocks.append(clean_block)
    return clean_markdown_blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown_block):
    heading_regex_pattern = r"^#{1,6} .+"
    code_regex_pattern = re.compile(r"^```\n(.*?)\n```$", re.DOTALL | re.MULTILINE)
    quote_regex_pattern = re.compile(r"(^>\s?.*(\n|$))+", re.MULTILINE)
    unordered_list_regex_patern = r"^- .+"
    ordered_list_regex_patern = r"^\d+\. .+"

    lines = markdown_block.split("\n")
    if len(lines) == 1 and re.match(heading_regex_pattern, lines[0]) is not None:
        return BlockType.HEADING

    if code_regex_pattern.match(markdown_block):
        return BlockType.CODE

    if quote_regex_pattern.match(markdown_block):
        return BlockType.QUOTE

    if all(re.match(unordered_list_regex_patern, line) for line in lines):
        return BlockType.UNORDERED_LIST

    line_number = 1
    is_ordered_list = True
    for line in lines:
        if re.match(ordered_list_regex_patern, line) is None:
            is_ordered_list = False
            break
        current_line_number = int(re.match(r"^\d+", line).group())
        if current_line_number != line_number:
            is_ordered_list = False
            break
        line_number += 1

    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
