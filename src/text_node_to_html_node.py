from textnode import TextType
from htmlnode import LeafNode



def text_node_to_html_node(text_node):
    text_type = text_node.text_type
    text = text_node.text
    url = text_node.url

    match text_type:
        case text_type.TEXT:
            return LeafNode(None, text)
        case text_type.BOLD:
            return LeafNode("b", text)
        case text_type.ITALIC:
            return LeafNode("i", text)
        case text_type.CODE:
            return LeafNode("code", text)
        case text_type.LINK:
            return LeafNode("a", text, {"href": url})
        case text_type.IMAGE:
            return LeafNode("img", "", {"src": url, "alt": text})
        case _:
            raise Exception(f"{text_type} is not supported text type")

