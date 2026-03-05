from text_node import TextNode, TextType
# from enum import Enum

# class DelemiterType(Enum):
    # TEXT = "text"
    # BOLD = "bold"
    # ITALIC = "italic"
    # CODE = "code"
    # LINK = "link"
    # IMAGE = "image"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if text_type != TextType.TEXT:
        for node in old_nodes:
            new_nodes.append(TextNode(
        return new_nodes

    new_nodes_type = None
    if delimiter == "**":
        new_nodes_type = TextType.BOLD
    if delimiter == "_":
        new_nodes_type = TextType.ITALIC
    if delimiter == "`":
        new_nodes_type = TextType.CODE

    if not new_nodes_type is None:
        splited_old_nodes = old_nodes.split(delimiter)
        new_nodes.append(splited_old_nodes[0])
        for not_text_node in splited_old_nodes[1:-1]:
            current_node = TextNode(
    

# class TextType(Enum):
    # TEXT = "text"
    # BOLD = "bold"
    # ITALIC = "italic"
    # CODE = "code"
    # LINK = "link"
    # IMAGE = "image"
# 
# 
# class TextNode:
