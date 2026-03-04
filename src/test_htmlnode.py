import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):

    def test_to_html_props(self):
        node = HTMLNode(
                "div",
                "Hello, world!",
                None,
                {"class": "greeting", "href": "https://boot.dev"},
                )
        self.assertEqual(
                node.props_to_html(),
                ' class="greeting" href="https://boot.dev"',
                )

    def test_values(self):
        node = HTMLNode(
                "div",
                "I wish I could read",
                )
        self.assertEqual(
                node.tag,
                "div",
                )
        self.assertEqual(
                node.value,
                "I wish I could read",
                )
        self.assertEqual(
                node.children,
                None,
                )
        self.assertEqual(
                node.props,
                None,
                )

    def test_repr(self):
        node = HTMLNode(
                "p",
                "What a strange world",
                None,
                {"class": "primary"},
                )
        self.assertEqual(
                node.__repr__(),
                "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
                )


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "hello, world!")
        self.assertEqual(node.to_html(), "<p>hello, world!</p>")

    def test_leaf_to_html_without_tag(self):
        node = LeafNode(None, "hello, world!")
        self.assertEqual(node.to_html(), "hello, world!")

    def test_leaf_to_html_bold(self):
        node = LeafNode("b", "hello, world!")
        self.assertEqual(node.to_html(), "<b>hello, world!</b>")

    def test_leaf_to_html_img_with_props(self):
        node = LeafNode("img", "hello, world!", {"src": "/home/user/Pictures/test_image1.png", "alt": "test image"})
        self.assertEqual(node.to_html(), '<img src="/home/user/Pictures/test_image1.png" alt="test image">hello, world!</img>')

    def test_leaf_to_html_link_with_props(self):
        node = LeafNode("a", "hello, world!", {"class": "greeting", "href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a class="greeting" href="https://boot.dev" target="_blank">hello, world!</a>')




if __name__ == "__main__":
    unittest.main()

