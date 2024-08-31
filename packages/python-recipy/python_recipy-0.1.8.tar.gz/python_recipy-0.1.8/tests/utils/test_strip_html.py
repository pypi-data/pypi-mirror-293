import unittest

from recipy.utils import strip_html


class TestStripHtml(unittest.TestCase):
    def test_basic_html_removal(self):
        self.assertEqual("Hello world", strip_html("<p>Hello world</p>"))
        self.assertEqual("Text with HTML tags", strip_html("<div>Text</div> with <span>HTML</span> tags"))
        self.assertEqual("Bold and Italic", strip_html("<b>Bold</b> and <i>Italic</i>"))

    def test_nested_html_tags(self):
        self.assertEqual("Nested HTML tags", strip_html("<div><p>Nested <span>HTML</span> tags</p></div>"))
        self.assertEqual("Item 1Item 2", strip_html("<ul><li>Item 1</li><li>Item 2</li></ul>"))

    def test_html_with_attributes(self):
        self.assertEqual("Link", strip_html('<a href="https://example.com">Link</a>'))
        self.assertEqual("", strip_html('<img src="image.jpg" alt="Image">'))

    def test_empty_html_tags(self):
        self.assertEqual("", strip_html("<div></div>"))
        self.assertEqual("", strip_html("<p><span></span></p>"))

    def test_no_html_tags(self):
        self.assertEqual("Just plain text", strip_html("Just plain text"))
        self.assertEqual("Another line of text", strip_html("Another line of text"))

    def test_malformed_html(self):
        self.assertEqual("Unclosed tag", strip_html("<p>Unclosed tag"))
        self.assertEqual("Some bold text", strip_html("Some <b>bold text"))
        self.assertEqual("Malformed HTML", strip_html("Malformed <div><p>HTML"))


if __name__ == '__main__':
    unittest.main()
