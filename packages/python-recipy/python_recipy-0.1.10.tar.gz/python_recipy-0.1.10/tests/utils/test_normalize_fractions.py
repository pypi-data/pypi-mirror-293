import unittest

from recipy.utils import normalize_fractions


class TestNormalizeFractions(unittest.TestCase):
    def test_unicode_fraction_to_ascii(self):
        self.assertEqual("1⁄2", normalize_fractions("½"))
        self.assertEqual("1⁄4", normalize_fractions("¼"))
        self.assertEqual("3⁄4", normalize_fractions("¾"))
        self.assertEqual("1⁄3", normalize_fractions("⅓"))
        self.assertEqual("2⁄3", normalize_fractions("⅔"))
        self.assertEqual("1⁄8", normalize_fractions("⅛"))
        self.assertEqual("3⁄8", normalize_fractions("⅜"))
        self.assertEqual("5⁄8", normalize_fractions("⅝"))
        self.assertEqual("7⁄8", normalize_fractions("⅞"))

    def test_mixed_numbers(self):
        self.assertEqual("1 1⁄2", normalize_fractions("1 1/2"))
        self.assertEqual("2 1⁄4", normalize_fractions("2 1/4"))
        self.assertEqual("3 3⁄4", normalize_fractions("3 3/4"))
        self.assertEqual("4 2⁄3", normalize_fractions("4 2/3"))

    def test_decimal_to_fraction(self):
        self.assertEqual("1⁄2", normalize_fractions("0.5"))
        self.assertEqual("1⁄4", normalize_fractions("0.25"))
        self.assertEqual("3⁄4", normalize_fractions("0.75"))
        self.assertEqual("1⁄3", normalize_fractions("0.333"))
        self.assertEqual("2⁄3", normalize_fractions("0.666"))
        self.assertEqual("1⁄8", normalize_fractions("0.125"))
        self.assertEqual("3⁄8", normalize_fractions("0.375"))
        self.assertEqual("5⁄8", normalize_fractions("0.625"))
        self.assertEqual("7⁄8", normalize_fractions("0.875"))

    def test_fraction_to_decimal(self):
        self.assertEqual("1⁄2", normalize_fractions("1/2"))
        self.assertEqual("1⁄4", normalize_fractions("1/4"))
        self.assertEqual("3⁄4", normalize_fractions("3/4"))
        self.assertEqual("1⁄3", normalize_fractions("1/3"))
        self.assertEqual("2⁄3", normalize_fractions("2/3"))
        self.assertEqual("1⁄8", normalize_fractions("1/8"))
        self.assertEqual("3⁄8", normalize_fractions("3/8"))
        self.assertEqual("5⁄8", normalize_fractions("5/8"))
        self.assertEqual("7⁄8", normalize_fractions("7/8"))

    def test_mixed_numbers_with_decimal_conversion(self):
        self.assertEqual("1 1⁄2", normalize_fractions("1 0.5"))
        self.assertEqual("2 1⁄4", normalize_fractions("2 0.25"))
        self.assertEqual("3 3⁄4", normalize_fractions("3 0.75"))
        self.assertEqual("4 1⁄3", normalize_fractions("4 0.333"))
        self.assertEqual("5 2⁄3", normalize_fractions("5 0.666"))
        self.assertEqual("6 1⁄8", normalize_fractions("6 0.125"))
        self.assertEqual("7 3⁄8", normalize_fractions("7 0.375"))
        self.assertEqual("8 5⁄8", normalize_fractions("8 0.625"))
        self.assertEqual("9 7⁄8", normalize_fractions("9 0.875"))

    def test_edge_cases(self):
        self.assertEqual("", normalize_fractions(""))
        self.assertEqual("No fractions here", normalize_fractions("No fractions here"))
        self.assertEqual("1 1⁄2 cups of sugar", normalize_fractions("1.5 cups of sugar"))
        self.assertEqual("1⁄4 cup", normalize_fractions("¼ cup"))
        self.assertEqual("1 1⁄2 cups", normalize_fractions("1 1/2 cups"))
        self.assertEqual("Some text 1⁄2 more text", normalize_fractions("Some text ½ more text"))

    def test_invalid_input(self):
        self.assertEqual("1 1/0", normalize_fractions("1 1/0"))  # Invalid fraction (division by zero)
        self.assertEqual("1.1.1", normalize_fractions("1.1.1"))  # Invalid decimal


if __name__ == '__main__':
    unittest.main()
