import unittest

from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):

    def simple_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        test_node1 = TextNode("This is text with a ", TextType.TEXT)
        test_node2 = TextNode("code block", TextType.CODE)
        test_node3 = TextNode(" word", TextType.TEXT)
        test_nodes = [test_node1, test_node2, test_node3]

        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i], test_nodes[i])

    # def test_eq_with_different_url(self):
        # node = TextNode("This is a text node", TextType.LINK)
        # node2 = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        # self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()

