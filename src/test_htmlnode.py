import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_repr(self):
        node = HtmlNode(tag="a", value="google", props={"href": "https://google.com"})
        self.assertEqual(
            node.__repr__(),
            "HtmlNode(a, google, None, {'href': 'https://google.com'})",
        )

    def test_creates_prop_string(self):
        test_cases = [
            (
                HtmlNode(tag="a", value="google", props={"href": "https://google.com"}),
                " href=https://google.com",
            ),
            (
                HtmlNode(
                    tag="a",
                    value="youtube",
                    props={"href": "http://youtube.com", "target": "_blank"},
                ),
                " href=http://youtube.com target=_blank",
            ),
            (
                HtmlNode(
                    "form",
                    None,
                    children=[HtmlNode("input", None, None, None)],
                    props={"type": "text", "id": "test"},
                ),
                " type=text id=test",
            ),
            (HtmlNode("h1", "Hello World", None, None), ""),
        ]

        for value, expected in test_cases:
            with self.subTest(value):
                self.assertEqual(value.props_to_html(), expected)


class TestLeafNode(unittest.TestCase):
    def test_creates_a_leaf_tag_with_props(self):
        leaf_node = LeafNode("a", "take action", {"href": "not.phishing.com"})
        self.assertEqual(
            leaf_node.to_html(), "<a href=not.phishing.com>take action</a>"
        )

    def test_creates_a_leaf_tag_without_props(self):
        leaf_node = LeafNode("h1", "hello")
        self.assertEqual(leaf_node.to_html(), "<h1>hello</h1>")

    def test_create_leaf_node_without_a_tag(self):
        leaf_node = LeafNode(None, "some value", None)
        self.assertEqual(leaf_node.to_html(), "some value")


class TestParentNode(unittest.TestCase):
    def test_creates_parent_node_with_children(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"

        self.assertEqual(parent_node.to_html(), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
