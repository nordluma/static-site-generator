import unittest

from htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    def test_repr(self):
        node = HtmlNode(tag="a", value="google", props={"href": "https://google.com"})
        self.assertEqual(
            node.__repr__(),
            "HtmlNode(a, google, None, {'href': 'https://google.com'})",
        )

    def creates_prop_string(self):
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
                    children=[
                        HtmlNode("input", None, None, {"type": "text", "id": "test"})
                    ],
                ),
                " type=text id=test",
            ),
            (HtmlNode("h1", "Hello World", None, None), ""),
        ]

        for value, expected in test_cases:
            with self.subTest(value):
                self.assertEqual(value.props_to_html(), expected)

