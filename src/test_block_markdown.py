import unittest

from block_markdown import markdown_to_blocks


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        test_cases = [
            (
                """
This is a **bolded** paragraph

This is another paragraph with a `code block`
and this is still the same paragraph

* This is a list
* with items
        """,
                [
                    "This is a **bolded** paragraph",
                    "This is another paragraph with a `code block`\nand this is still the same paragraph",
                    "* This is a list\n* with items",
                ],
            ),
            (
                """
# This is a heading

A paragraph
in three
lines

* a list with a single item
            """,
                [
                    "# This is a heading",
                    "A paragraph\nin three\nlines",
                    "* a list with a single item",
                ],
            ),
        ]

        for text, expected in test_cases:
            actual = markdown_to_blocks(text)
            with self.subTest(actual):
                self.assertListEqual(actual, expected)
