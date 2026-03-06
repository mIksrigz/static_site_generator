from textnode import TextNode, TextType


delimiters = {
        "**": TextType.BOLD,
        "_": TextType.ITALIC,
        "`": TextType.CODE
        }

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    text_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            text_nodes.append(old_node)
            continue
        if delimiter not in delimiters:
            raise Exception(f"Cannot process provided delimeter: {delimiter}")

        splited_text = old_node.text.split(delimiter)
        if len(splited_text) % 2 == 0:
            raise Exception(f"{delimiter} didn't have a closing pair")

        for i in range(len(splited_text)):
            if i % 2 == 0:
                text_nodes.append(TextNode(splited_text[i], TextType.TEXT))
            else:
                text_nodes.append(TextNode(splited_text[i], text_type))

    return text_nodes


