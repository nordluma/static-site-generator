import unittest

from htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    def test_repr(self):
        node = HtmlNode(tag="<a>", value="google", props={"href": "https://google.com"})
        self.assertEqual(
            node.__repr__(),
            "HtmlNode(<a>, google, None, {'href': 'https://google.com'})",
        )

