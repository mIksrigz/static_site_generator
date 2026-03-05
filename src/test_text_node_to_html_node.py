import unittest

from textnode import TextNode, TextType
from text_node_to_html_node import text_node_to_html_node


class TestTextToHtml(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})


    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, "/home/user/pictures/test_image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "/home/user/pictures/test_image.png", "alt": node.text})
# /home/miksr/workspace/bootdotdev
        # case text_type.TEXT:
            # return LeafNode(None, text)
        # case text_type.BOLD:
            # return LeafNode("b", text)
        # case text_type.ITALIC:
            # return LeafNode("i", text)
        # case text_type.CODE:
            # return LeafNode("code", text)
        # case text_type.LINK:
            # return LeafNode("a", text, {"href": url})
        # case text_type.IMAGE:
            # return LeafNode("img", "", {"src": url, "alt": text})
        # case _:
            # raise Exception(f"{text_type} is not supported text type")

if __name__ == "__main__":
    unittest.main()

