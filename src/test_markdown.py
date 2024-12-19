import unittest

from markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
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

    def test_split_image(self):
        test_cases = [
            (
                TextNode(
                    "This is a text node with an ![image](https://url.com/file.jpg)",
                    TextType.TEXT,
                ),
                [
                    TextNode("This is a text node with an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://url.com/file.jpg"),
                ],
            ),
            (
                TextNode("![image](test.gif)", TextType.TEXT),
                [TextNode("image", TextType.IMAGE, "test.gif")],
            ),
            (
                TextNode(
                    "This has a ![image](test.jpg) and ![another](second.png)",
                    TextType.TEXT,
                ),
                [
                    TextNode("This has a ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "test.jpg"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("another", TextType.IMAGE, "second.png"),
                ],
            ),
        ]
        for node, expected in test_cases:
            new_nodes = split_nodes_image([node])
            with self.subTest(new_nodes):
                self.assertListEqual(new_nodes, expected)

    def test_split_link(self):
        test_cases = [
            (
                TextNode(
                    "This is a text node with an [link](https://url.com/file.jpg)",
                    TextType.TEXT,
                ),
                [
                    TextNode("This is a text node with an ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://url.com/file.jpg"),
                ],
            ),
            (
                TextNode("[link](test.gif)", TextType.TEXT),
                [TextNode("link", TextType.LINK, "test.gif")],
            ),
            (
                TextNode(
                    "This has a [link](youtube.com) and [another](google.com)",
                    TextType.TEXT,
                ),
                [
                    TextNode("This has a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "youtube.com"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("another", TextType.LINK, "google.com"),
                ],
            ),
        ]
        for node, expected in test_cases:
            new_nodes = split_nodes_link([node])
            with self.subTest(new_nodes):
                self.assertListEqual(new_nodes, expected)

    def test_text_to_textnode(self):
        test_cases = [
            (
                "This is a **sentence** with *all* kinds of `styles` including ![images](test.jpg) and [links](test.com)",
                [
                    TextNode("This is a ", TextType.TEXT),
                    TextNode("sentence", TextType.BOLD),
                    TextNode(" with ", TextType.TEXT),
                    TextNode("all", TextType.ITALIC),
                    TextNode(" kinds of ", TextType.TEXT),
                    TextNode("styles", TextType.CODE),
                    TextNode(" including ", TextType.TEXT),
                    TextNode("images", TextType.IMAGE, "test.jpg"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("links", TextType.LINK, "test.com"),
                ],
            ),
            (
                "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
                [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode(
                        "obi wan image",
                        TextType.IMAGE,
                        "https://i.imgur.com/fJRm4Vk.jpeg",
                    ),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ],
            ),
        ]

        for text, expected in test_cases:
            nodes = text_to_textnodes(text)
            with self.subTest(nodes):
                self.assertListEqual(
                    nodes,
                    expected,
                )
