import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_with_different_type(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_with_different_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_with_different_url(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_eq_with_equal_url(self):
        node = TextNode("This is a text node", TextType.IMAGE, "/home/miksr/images/image1.png")
        node2 = TextNode("This is a text node", TextType.IMAGE, "/home/miksr/images/image1.png")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
                        "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
                        )

if __name__ == "__main__":
    unittest.main()

