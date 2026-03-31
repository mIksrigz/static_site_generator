import re

from textnode import TextNode, TextType

delimiters = {"**": TextType.BOLD, "_": TextType.ITALIC, "`": TextType.CODE}


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return matches


def text_to_textnodes(text):

    starting_text_node = TextNode(text, TextType.TEXT)
    after_bold = split_nodes_delimiter([starting_text_node], "**", TextType.BOLD)
    after_italic = split_nodes_delimiter(after_bold, "_", TextType.ITALIC)
    after_code = split_nodes_delimiter(after_italic, "`", TextType.CODE)
    after_image = split_nodes_image(after_code)
    after_link = split_nodes_link(after_image)

    return after_link


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        if delimiter not in delimiters:
            raise Exception(f"Cannot process provided delimeter: {delimiter}")

        splited_text = old_node.text.split(delimiter)
        if len(splited_text) % 2 == 0:
            raise Exception(f"{delimiter} didn't have a closing pair")

        for i in range(len(splited_text)):
            if splited_text[i] == "":
                continue
            if i % 2 == 0:
                result.append(TextNode(splited_text[i], TextType.TEXT))
            else:
                result.append(TextNode(splited_text[i], text_type))

    return result


def split_nodes_link(old_nodes):
    result = []
    for old_node in old_nodes:
        if old_node.text == "":
            continue

        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        alt_text_and_url = extract_markdown_links(old_node.text)

        if len(alt_text_and_url) < 1:
            result.append(old_node)
            continue

        current_text = old_node.text
        for atl_text_url_pair in alt_text_and_url:
            alt_text, url = atl_text_url_pair
            full_markdown = f"[{alt_text}]({url})"

            current_text = current_text.split(full_markdown, maxsplit=1)
            if len(current_text) > 1:
                if current_text[0] != "":
                    result.append(TextNode(current_text[0], TextType.TEXT))
                current_text = str(current_text[1:][0])

            result.append(TextNode(alt_text, TextType.LINK, url))
        if current_text != "":
            result.append(TextNode(current_text, TextType.TEXT))
    return result


def split_nodes_image(old_nodes):
    result = []
    for old_node in old_nodes:
        if old_node.text == "":
            continue

        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        alt_text_and_url = extract_markdown_images(old_node.text)

        if len(alt_text_and_url) < 1:
            result.append(old_node)
            continue

        current_text = old_node.text
        for atl_text_url_pair in alt_text_and_url:
            alt_text, url = atl_text_url_pair
            full_markdown = f"![{alt_text}]({url})"

            current_text = current_text.split(full_markdown, maxsplit=1)
            if len(current_text) > 1:
                if current_text[0] != "":
                    result.append(TextNode(current_text[0], TextType.TEXT))
                current_text = str(current_text[1:][0])

            result.append(TextNode(alt_text, TextType.IMAGE, url))

        if current_text != "":
            result.append(TextNode(current_text, TextType.TEXT))
    return result
