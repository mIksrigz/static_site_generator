from enum import Enum

class TextType(Enum):
    # text = ""
    # **Bold text**
    # _Italic text_
    # Links, in this format: [anchor text](url)
    # Images, in this format: ![alt text](url)

    TEXT = ""
    BOLD_TEXT = "**"
    ITALIC_TEXT = "__"
    LINKS = "[]()"
    IMAGES = "![]()"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
                    self.text == other.text and
                    self.text_type == other.text_type and
                    self.url == url
                )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
