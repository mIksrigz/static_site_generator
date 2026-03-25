import unittest

from inline_markdown import (
    split_nodes_delimiter, 
    split_nodes_link, 
    split_nodes_image, 
    extract_markdown_images, 
    extract_markdown_links, 
    text_to_textnodes
)
from textnode import TextNode, TextType


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

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


class Test_Extract_Markdown_Images(unittest.TestCase):
    def test_image_markdown(self):
        text = "![test text](/home/user/Pictures/img1.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("test text", "/home/user/Pictures/img1.png")],
            matches
        )

    def test_two_image_markdown(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")],
            matches
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)



class Test_Extract_Markdown_Links(unittest.TestCase):
    def test_link_markdown(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],
            matches
        )


class Test_Split_Nodes_Link(unittest.TestCase):
    def test_double_link_markdown(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]

    def test_start_double_link_markdown(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://wikipedia.org"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )


class Test_Split_Nodes_Image(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_start_double_image_markdown(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

class Test_Text_To_Textnodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            result
        )

    def test_image_and_link(self):
        text = "![logo](https://example.com/logo.png) see [docs](https://docs.example.com)"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("logo", TextType.IMAGE, "https://example.com/logo.png"),
                TextNode(" see ", TextType.TEXT),
                TextNode("docs", TextType.LINK, "https://docs.example.com"),
            ],
            result
        )

    def test_code_between_text(self):
        text = "Run `npm install` to get started"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Run ", TextType.TEXT),
                TextNode("npm install", TextType.CODE),
                TextNode(" to get started", TextType.TEXT),
            ],
            result
        )

    def test_empty_string(self):
        text = ""
        result = text_to_textnodes(text)
        self.assertListEqual([], result)

    def test_bold_italic_code(self):
        text = "**bold** then _italic_ then `code`"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" then ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" then ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
            result
        )

    def test_bold_wrapping_link(self):
        text = "Check **this** and [a link](https://example.com) together"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Check ", TextType.TEXT),
                TextNode("this", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "https://example.com"),
                TextNode(" together", TextType.TEXT),
            ],
            result
        )

    def test_code_and_image_and_link(self):
        text = "Run `git clone` then see ![diagram](https://example.com/d.png) and [docs](https://docs.example.com)"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Run ", TextType.TEXT),
                TextNode("git clone", TextType.CODE),
                TextNode(" then see ", TextType.TEXT),
                TextNode("diagram", TextType.IMAGE, "https://example.com/d.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("docs", TextType.LINK, "https://docs.example.com"),
            ],
            result
        )

    def test_italic_code_link(self):
        text = "_Note:_ use `pip install` and see [PyPI](https://pypi.org)"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Note:", TextType.ITALIC),
                TextNode(" use ", TextType.TEXT),
                TextNode("pip install", TextType.CODE),
                TextNode(" and see ", TextType.TEXT),
                TextNode("PyPI", TextType.LINK, "https://pypi.org"),
            ],
            result
        )

    def test_image_between_bold_and_italic(self):
        text = "**Start** ![pic](https://example.com/pic.jpg) _end_"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Start", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("pic", TextType.IMAGE, "https://example.com/pic.jpg"),
                TextNode(" ", TextType.TEXT),
                TextNode("end", TextType.ITALIC),
            ],
            result
        )

    def test_two_codes_and_two_links(self):
        text = "Use `cd` or `ls` to navigate, see [man](https://man7.org) or [tldr](https://tldr.sh)"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Use ", TextType.TEXT),
                TextNode("cd", TextType.CODE),
                TextNode(" or ", TextType.TEXT),
                TextNode("ls", TextType.CODE),
                TextNode(" to navigate, see ", TextType.TEXT),
                TextNode("man", TextType.LINK, "https://man7.org"),
                TextNode(" or ", TextType.TEXT),
                TextNode("tldr", TextType.LINK, "https://tldr.sh"),
            ],
            result
        )

    def test_all_types_no_plain_text_between(self):
        text = "**bold**_italic_`code`[link](https://example.com)![img](https://example.com/img.png)"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode("img", TextType.IMAGE, "https://example.com/img.png"),
            ],
            result
        )


if __name__ == "__main__":
    unittest.main()
