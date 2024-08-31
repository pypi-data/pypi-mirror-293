import unittest
from tgentity import to_html
from tgentity.types import Message, MessageEntity


HTML_test = "URL entity inside bold must stringify to HTML correctly"


class TestHTML(unittest.TestCase):
    print("Testing HTML")
    print(f"API: \n  {Message=}\n  {MessageEntity=}\n\n")

    def test_html(self):
        assert (
            to_html(
                Message(
                    id=0,
                    text="Hello, https://feathers.studio!",
                    entities=[
                        MessageEntity(
                            type="bold",
                            offset=0,
                            length=len("Hello, https://feathers.studio!"),
                        ),
                        MessageEntity(
                            type="url",
                            offset=len("Hello, "),
                            length=len("https://feathers.studio"),
                        ),
                    ],
                )
            )
            == '<b>Hello, <a href="https://feathers.studio">https://feathers.studio</a>!</b>'
        ), HTML_test

        assert (
            to_html(
                Message(
                    id=0,
                    text="Hello, feathers.studio!",
                    entities=[
                        MessageEntity(
                            type="bold", offset=0, length=len("Hello, feathers.studio!")
                        ),
                        MessageEntity(
                            type="text_link",
                            offset=len("Hello, "),
                            length=len("feathers.studio"),
                            url="https://feathers.studio",
                        ),
                    ],
                )
            )
            == '<b>Hello, <a href="https://feathers.studio">feathers.studio</a>!</b>'
        ), HTML_test

        assert (
            to_html(
                Message(
                    id=0,
                    text="👉 Link :- https://example.com?x&y",
                    entities=[
                        MessageEntity(offset=0, length=10, type="bold"),
                        MessageEntity(offset=10, length=23, type="url"),
                        MessageEntity(offset=10, length=23, type="bold"),
                    ],
                )
            )
            == '<b>👉 Link :- </b><a href="https://example.com?x&y"><b>https://example.com?x&amp;y</b></a>'
        ), HTML_test

        assert (
            to_html(
                Message(
                    id=0,
                    text="Blockquote",
                    entities=[
                        MessageEntity(
                            offset=0, length=len("Blockquote"), type="blockquote"
                        )
                    ],
                )
            )
            == "<blockquote>Blockquote</blockquote>"
        ), HTML_test

        assert (
            to_html(
                Message(
                    id=0,
                    text="❗️",
                    entities=[
                        MessageEntity(
                            offset=0,
                            length=len("❗️"),
                            type="custom_emoji",
                            custom_emoji_id="5445331903496332384",
                        )
                    ],
                )
            )
            == '<tg-emoji emoji-id="5445331903496332384">❗️</tg-emoji>'
        ), HTML_test

        assert (
            to_html(
                Message(
                    id=0,
                    text="Blockquote\n\nBlockquote",
                    entities=[
                        MessageEntity(
                            type="blockquote",
                            offset=0,
                            length=len("Blockquote\n\nBlockquote"),
                        )
                    ],
                )
            )
            == "<blockquote>Blockquote\n\nBlockquote</blockquote>"
        ), HTML_test


if __name__ == "__main__":
    unittest.main()
