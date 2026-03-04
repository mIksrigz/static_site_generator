import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode


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

# LEAF NODES TESTS

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



# PARENT NODES TESTS


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_children_and_props(self):
        child_node = LeafNode("img", "", {"src": "/home/user/Pictures/test_image1.png", "alt": "test image"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><img src="/home/user/Pictures/test_image1.png" alt="test image"></img></div>')
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
                parent_node.to_html(),
                "<div><span><b>grandchild</b></span></div>",
                )

    def test_to_html_with_grandchildren_and_props(self):
        link_element1 = LeafNode("a", "home", {"class": "no-text-decoration"})
        link_element2 = LeafNode("a", "about", {"class": "no-text-decoration"})
        link_element3 = LeafNode("a", "contact", {"class": "no-text-decoration"})

        list_element1 = ParentNode("li", [link_element1], {"class": "no-padding"}) 
        list_element2 = ParentNode("li", [link_element2], {"class": "no-padding"}) 
        list_element3 = ParentNode("li", [link_element3], {"class": "no-padding"}) 
        list_elements = [list_element1, list_element2, list_element3]

        unordered_list = ParentNode("ul", list_elements)
        nav_element = ParentNode("nav", [unordered_list])
        self.assertEqual(
                nav_element.to_html(),
                '<nav><ul><li class="no-padding"><a class="no-text-decoration">home</a></li><li class="no-padding"><a class="no-text-decoration">about</a></li><li class="no-padding"><a class="no-text-decoration">contact</a></li></ul></nav>',
                )


if __name__ == "__main__":
    unittest.main()

