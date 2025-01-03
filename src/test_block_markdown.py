import unittest

from block_markdown import (
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


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

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here
"""

        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items
"""

        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is a paragraph text

## this is an h2
"""

        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is a paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is a paragraph text
"""

        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is a paragraph text</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
