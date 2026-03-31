import unittest

from markdown_blocks import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class Test_Markdown_To_Blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_block(self):
        md = """
Just one paragraph here
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one paragraph here"])

    def test_extra_blank_lines_between_blocks(self):
        md = """
First block


Second block



Third block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block", "Third block"])

    def test_heading_and_paragraph(self):
        md = """
# Heading one

Some paragraph text beneath it
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading one", "Some paragraph text beneath it"])

    def test_multiple_headings(self):
        md = """
# Title

## Subtitle

### Section
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Title", "## Subtitle", "### Section"])

    def test_ordered_list_block(self):
        md = """
Some intro text

1. First item
2. Second item
3. Third item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Some intro text",
                "1. First item\n2. Second item\n3. Third item",
            ],
        )

    def test_blockquote_and_paragraph(self):
        md = """
> This is a blockquote
> spanning two lines

And a follow-up paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "> This is a blockquote\n> spanning two lines",
                "And a follow-up paragraph",
            ],
        )

    def test_heading_list_and_paragraph(self):
        md = """
## Shopping List

- Apples
- Bananas
- Cherries

Don't forget the milk!
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "## Shopping List",
                "- Apples\n- Bananas\n- Cherries",
                "Don't forget the milk!",
            ],
        )

    def test_whitespace_only_lines_ignored(self):
        md = "First block\n   \n\nSecond block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])


class Test_Block_To_Block_Type(unittest.TestCase):
    # HEADING
    def test_block_to_block_type_heading(self):
        self.assertEqual(
            block_to_block_type("### This is test Heading"), BlockType.HEADING
        )

    def test_block_to_block_type_heading_h1(self):
        self.assertEqual(block_to_block_type("# H1 Heading"), BlockType.HEADING)

    def test_block_to_block_type_heading_h6(self):
        self.assertEqual(block_to_block_type("###### H6 Heading"), BlockType.HEADING)

    def test_block_to_block_type_heading_too_many_hashes(self):
        self.assertEqual(
            block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_heading_no_space(self):
        self.assertEqual(block_to_block_type("###NoSpace"), BlockType.PARAGRAPH)

    # CODE
    def test_block_to_block_type_code(self):
        self.assertEqual(block_to_block_type("```\nsome code\n```"), BlockType.CODE)

    def test_block_to_block_type_code_multiline(self):
        self.assertEqual(
            block_to_block_type("```\nline one\nline two\n```"), BlockType.CODE
        )

    def test_block_to_block_type_code_missing_closing(self):
        self.assertEqual(block_to_block_type("```\nsome code"), BlockType.PARAGRAPH)

    # QUOTE
    def test_block_to_block_type_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)

    def test_block_to_block_type_quote_multiline(self):
        self.assertEqual(block_to_block_type("> line one\n> line two"), BlockType.QUOTE)

    def test_block_to_block_type_quote_no_space(self):
        self.assertEqual(block_to_block_type(">no space quote"), BlockType.QUOTE)

    def test_block_to_block_type_not_quote(self):
        self.assertEqual(
            block_to_block_type("This is not a quote"), BlockType.PARAGRAPH
        )

    # UNORDERED LIST
    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- item one\n- item two\n- item three"),
            BlockType.UNORDERED_LIST,
        )

    def test_block_to_block_type_unordered_list_single(self):
        self.assertEqual(block_to_block_type("- single item"), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_missing_dash(self):
        self.assertEqual(
            block_to_block_type("- item one\nitem two"), BlockType.PARAGRAPH
        )

    # ORDERED LIST
    def test_block_to_block_type_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. first\n2. second\n3. third"),
            BlockType.ORDERED_LIST,
        )

    def test_block_to_block_type_ordered_list_single(self):
        self.assertEqual(block_to_block_type("1. only item"), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_wrong_start(self):
        self.assertEqual(
            block_to_block_type("2. first\n3. second"), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_ordered_list_out_of_order(self):
        self.assertEqual(
            block_to_block_type("1. first\n3. second"), BlockType.PARAGRAPH
        )

    # PARAGRAPH
    def test_block_to_block_type_paragraph(self):
        self.assertEqual(
            block_to_block_type("Just a plain paragraph."), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_paragraph_multiline(self):
        self.assertEqual(block_to_block_type("line one\nline two"), BlockType.PARAGRAPH)


class Test_Markdown_To_Html_Node(unittest.TestCase):
    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
