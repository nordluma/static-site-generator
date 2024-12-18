import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node_1 = TextNode("This is a text node", TextType.BOLD)
        node_2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node_1, node_2)


class TestConvertTextNodeToLeafNode(unittest.TestCase):
    def test_convert_normal_to_leafnode(self):
        self.assertEqual(
            text_node_to_html_node(TextNode("normal text", TextType.TEXT)),
            LeafNode(None, "normal text"),
        )

    def test_convert_bold_to_leafnode(self):
        self.assertEqual(
            text_node_to_html_node(TextNode("bold text", TextType.BOLD)),
            LeafNode("b", "bold text"),
        )

    def test_convert_italic_to_leafnode(self):
        self.assertEqual(
            text_node_to_html_node(TextNode("italic text", TextType.ITALIC)),
            LeafNode("i", "italic text"),
        )

    def test_convert_code_to_leafnode(self):
        self.assertEqual(
            text_node_to_html_node(TextNode("code text", TextType.CODE)),
            LeafNode("code", "code text"),
        )

    def test_convert_link_to_leafnode(self):
        self.assertEqual(
            text_node_to_html_node(
                TextNode("anchor text", TextType.LINK, "example.com")
            ),
            LeafNode("a", "anchor text", {"href": "example.com"}),
        )

    def test_convert_image_to_leafnode(self):
        self.assertEqual(
            text_node_to_html_node(TextNode("alt text", TextType.IMAGE, "image.jpg")),
            LeafNode("img", "", {"src": "image.jpg", "alt": "alt text"}),
        )

    # We do not need this test for now since we are using type hints
    """
    def test_convert_invalid_texttype_to_leafnode(self):
        self.assertRaises(
            text_node_to_html_node(TextNode("text", TextType.Invalid, None))
        )
    """


if __name__ == "__main__":
    unittest.main()
