import unittest

from block_markdown import block_to_block_type, markdown_to_blocks


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

    def test_block_to_block_type(self):
        test_cases = [
            ("# heading 1", "heading"),
            ("## heading 2", "heading"),
            ("### heading 3", "heading"),
            ("#### heading 4", "heading"),
            ("##### heading 5", "heading"),
            ("###### heading 6", "heading"),
            ('```python\nprint("hello, world")\n```', "code"),
            ('```console.log("hello, world")```', "code"),
            (">to be\n>or not to be", "quote"),
            ("* this is a list\n* with items", "unordered_list"),
            ("- another list\n- with items", "unordered_list"),
            ("* list with different\n- starting symbols", "unordered_list"),
            ("1. one\n2. two\n3. three", "ordered_list"),
            ("a normal paragraph", "paragraph"),
        ]

        for block, expected in test_cases:
            actual = block_to_block_type(block)
            with self.subTest(actual):
                self.assertEqual(actual, expected, f"when block was {block}")
