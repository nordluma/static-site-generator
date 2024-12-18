import unittest

from conversion import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)
from textnode import TextNode, TextType


class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_with_code_delim(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(actual, expected)

    def test_split_nodes_with_bold_delim(self):
        node = TextNode("This contains a **very** important part", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This contains a ", TextType.TEXT),
            TextNode("very", TextType.BOLD),
            TextNode(" important part", TextType.TEXT),
        ]
        self.assertListEqual(actual, expected)

    def test_split_nodes_with_italic_delim(self):
        node = TextNode("This contains some *fancy* text", TextType.TEXT)
        actual = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This contains some ", TextType.TEXT),
            TextNode("fancy", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(actual, expected)

    def test_split_nodes_with_double_delims(self):
        node = TextNode(
            "This has **a very** important message **don't** forget it",
            TextType.TEXT,
        )
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("a very", TextType.BOLD),
            TextNode(" important message ", TextType.TEXT),
            TextNode("don't", TextType.BOLD),
            TextNode(" forget it", TextType.TEXT),
        ]
        self.assertListEqual(actual, expected)

    def test_split_nodes_with_multi_delims(self):
        node = TextNode(
            "This contains some *fancy* words and a `code block` word", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        actual = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        expected = [
            TextNode("This contains some ", TextType.TEXT),
            TextNode("fancy", TextType.ITALIC),
            TextNode(" words and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(actual, expected)

    def test_extract_markdown_images(self):
        test_cases = [
            ("this is markdown with an ![image](url.com)", [("image", "url.com")]),
            (
                "this has ![multiple](image.com) images in the ![same](sentence.fi)",
                [("multiple", "image.com"), ("same", "sentence.fi")],
            ),
            ("this test has a [link](test.rs) instead of image", []),
            (
                "this has a [link](test.rs) first and then an ![image](picz.com)",
                [("image", "picz.com")],
            ),
        ]

        for text, expected in test_cases:
            actual = extract_markdown_images(text)
            with self.subTest(actual):
                self.assertListEqual(actual, expected)

    def test_extract_markdown_links(self):
        test_cases = [
            (
                "this is markdown with a [link](somesite.com)",
                [("link", "somesite.com")],
            ),
            (
                "this has [multiple](test_site.com) links in the [text](whatamidoing.fi)",
                [("multiple", "test_site.com"), ("text", "whatamidoing.fi")],
            ),
            ("this has an ![image](plz.com) instead of a link", []),
            (
                "this has an ![image](testing_stuff.rs) and a [link](this_should_be_enough.org)",
                [("link", "this_should_be_enough.org")],
            ),
        ]

        for text, expected in test_cases:
            actual = extract_markdown_links(text)
            with self.subTest(actual):
                self.assertListEqual(actual, expected)
