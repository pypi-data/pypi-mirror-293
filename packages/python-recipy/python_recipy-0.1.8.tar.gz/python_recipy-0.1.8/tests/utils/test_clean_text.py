import unittest

from recipy.utils import clean_text


class TestCleanText(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual("", clean_text(""))

    def test_basic_cleaning(self):
        self.assertEqual("Tom & Jerry", clean_text("Tom &amp; Jerry"))
        self.assertEqual("Bake at 350°F for 30 minutes", clean_text("Bake at 350 degrees F for 30 minutes"))
        self.assertEqual("Add 1⁄2 cup of sugar", clean_text("Add 1/2 cup of sugar"))

    def test_combined_operations(self):
        self.assertEqual("350°F & 1⁄2 tsp salt", clean_text("  350 degrees F   &amp;  1/2 tsp salt  "))
        self.assertEqual("180°C and 3⁄4 cup milk", clean_text("180 degrees C and ¾ cup milk"))

    def test_whitespace_handling(self):
        self.assertEqual("Leading and trailing spaces", clean_text("   Leading and trailing spaces   "))
        self.assertEqual("Multiple spaces collapsed", clean_text("Multiple    spaces    collapsed"))
        self.assertEqual("Newline and tab handling", clean_text("Newline\nand\ttab handling"))

    def test_html_entities_and_fractions(self):
        self.assertEqual("1⁄2 cup of sugar & 3⁄4 tsp salt", clean_text("1/2 cup of sugar &amp; 3/4 tsp salt"))
        self.assertEqual("Mix 2⁄3 cup flour", clean_text("Mix 2/3 cup flour"))

    def test_edge_cases(self):
        self.assertEqual("0°F", clean_text("0 degrees F"))
        self.assertEqual("-10°C and 1⁄8 tsp", clean_text("-10 degrees C and 1/8 tsp"))
        self.assertEqual("No temperature or fraction", clean_text("No temperature or fraction"))

    def test_invalid_input_handling(self):
        self.assertEqual("Invalid fraction 1/0", clean_text("Invalid fraction 1/0"))


if __name__ == '__main__':
    unittest.main()
