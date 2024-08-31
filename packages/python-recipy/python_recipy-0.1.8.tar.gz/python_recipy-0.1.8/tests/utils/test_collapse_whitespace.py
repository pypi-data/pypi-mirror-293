import unittest

from recipy.utils import collapse_whitespace


class TestCollapseWhitespace(unittest.TestCase):
    def test_collapse_newlines(self):
        self.assertEqual("Line 1 Line 2", collapse_whitespace("Line 1\nLine 2"))
        self.assertEqual("Line 1 Line 2", collapse_whitespace("Line 1\rLine 2"))
        self.assertEqual("Line 1 Line 2", collapse_whitespace("Line 1\n\rLine 2"))

    def test_collapse_tabs(self):
        self.assertEqual("Tabbed text", collapse_whitespace("Tabbed\ttext"))
        self.assertEqual("Multiple tabs in text", collapse_whitespace("Multiple\ttabs\tin\ttext"))

    def test_collapse_spaces(self):
        self.assertEqual("Single space", collapse_whitespace("Single    space"))
        self.assertEqual("Leading and trailing spaces", collapse_whitespace("   Leading and trailing spaces   "))

    def test_collapse_mixed_whitespace(self):
        self.assertEqual("Mixed whitespace text", collapse_whitespace("Mixed \n \r \t whitespace text"))
        self.assertEqual("Text with various whitespace", collapse_whitespace("\tText \nwith \rvarious \t\n\rwhitespace"))

    def test_zero_width_space(self):
        self.assertEqual("Text with zero width space", collapse_whitespace("Text\u200Bwith\u200Bzero\u200Bwidth\u200Bspace"))

    def test_non_breaking_space(self):
        self.assertEqual("Text with non breaking space", collapse_whitespace("Text\xA0with\xA0non\xA0breaking\xA0space"))

    def test_empty_string(self):
        self.assertEqual("", collapse_whitespace(""))

    def test_no_operation_needed(self):
        self.assertEqual("No changes needed", collapse_whitespace("No changes needed"))


if __name__ == '__main__':
    unittest.main()
