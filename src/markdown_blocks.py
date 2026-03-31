import re
from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


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
    code_regex_pattern = re.compile(r"^```\n(.*?)\n```\Z", re.DOTALL)
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


def markdown_to_html_node(markdown):
    all_html_nodes = []
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        block = "\n".join(line.strip() for line in block.split("\n"))
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            prepared_text = " ".join(line.strip() for line in block.split("\n"))
            text_nodes = text_to_textnodes(prepared_text)
            html_nodes = []
            for text_node in text_nodes:
                html_node = text_node_to_html_node(text_node)
                html_nodes.append(html_node)
            all_html_nodes.append(ParentNode("p", html_nodes))

        if block_type == BlockType.HEADING:
            heading_size = 0
            text_content = block
            while text_content.startswith("#"):
                heading_size += 1
                text_content = text_content[1:]
            text_content = text_content.strip()

            prepared_text = " ".join(text_content.split("\n"))
            text_nodes = text_to_textnodes(prepared_text)
            html_nodes = []
            for text_node in text_nodes:
                html_node = text_node_to_html_node(text_node)
                html_nodes.append(html_node)
            heading_tag = f"h{heading_size}"
            all_html_nodes.append(ParentNode(heading_tag, html_nodes))

        if block_type == BlockType.CODE:
            text_content = "\n".join(block.split("\n")[1:-1]) + "\n"
            text_node = TextNode(text_content, TextType.CODE)
            code_html_node = text_node_to_html_node(text_node)
            wrapper = ParentNode("pre", [code_html_node])
            all_html_nodes.append(wrapper)

        if block_type == BlockType.UNORDERED_LIST:
            list_content = block
            list_item = list_content.split("\n")
            html_inside_unordered_list = []
            for item in list_item:
                item = item[2:]
                item_contents = text_to_textnodes(item)
                html_inside_list_item = []
                for item_content in item_contents:
                    item_content_html = text_node_to_html_node(item_content)
                    html_inside_list_item.append(item_content_html)
                list_item_html_node = ParentNode("li", html_inside_list_item)
                html_inside_unordered_list.append(list_item_html_node)

            unordered_list_html_node = ParentNode("ul", html_inside_unordered_list)
            all_html_nodes.append(unordered_list_html_node)

        if block_type == BlockType.ORDERED_LIST:
            list_content = block
            list_item = list_content.split("\n")
            html_inside_ordered_list = []
            for item in list_item:
                prefix = re.match(r"^\d+\. ", item).group()
                item = item[len(prefix) :]
                item_contents = text_to_textnodes(item)
                html_inside_list_item = []
                for item_content in item_contents:
                    item_content_html = text_node_to_html_node(item_content)
                    html_inside_list_item.append(item_content_html)
                list_item_html_node = ParentNode("li", html_inside_list_item)
                html_inside_ordered_list.append(list_item_html_node)

            ordered_list_html_node = ParentNode("ol", html_inside_ordered_list)
            all_html_nodes.append(ordered_list_html_node)

        if block_type == BlockType.QUOTE:
            quote_lines = block.split("\n")
            clean_quote_lines = []
            for quote_line in quote_lines:
                prefix = re.match(r"^> ?", quote_line).group()
                if len(prefix) == 2:
                    clean_quote_lines.append(quote_line[2:])
                else:
                    clean_quote_lines.append(quote_line[1:])

            text_content = " ".join(clean_quote_lines)
            text_nodes = text_to_textnodes(text_content)
            inner_html_nodes = []
            for text_node in text_nodes:
                html_node = text_node_to_html_node(text_node)
                inner_html_nodes.append(html_node)
            html_quote_node = ParentNode("blockquote", inner_html_nodes)
            all_html_nodes.append(html_quote_node)

    return ParentNode("div", all_html_nodes)
