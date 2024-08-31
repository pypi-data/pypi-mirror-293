import unittest

from recipy.utils import normalize_temperatures


class TestNormalizeTemperatures(unittest.TestCase):
    def test_fahrenheit_normalization(self):
        self.assertEqual("350°F", normalize_temperatures("350 degrees F"))
        self.assertEqual("212°F", normalize_temperatures("212 degrees F"))
        self.assertEqual("100°F", normalize_temperatures("100 degrees F"))

    def test_celsius_normalization(self):
        self.assertEqual("180°C", normalize_temperatures("180 degrees C"))
        self.assertEqual("100°C", normalize_temperatures("100 degrees C"))
        self.assertEqual("0°C", normalize_temperatures("0 degrees C"))

    def test_mixed_temperatures(self):
        self.assertEqual("Bake at 350°F and then reduce to 180°C", normalize_temperatures("Bake at 350 degrees F and then reduce to 180 degrees C"))
        self.assertEqual("Start with 212°F and cool to 0°C", normalize_temperatures("Start with 212 degrees F and cool to 0 degrees C"))

    def test_no_normalization_needed(self):
        self.assertEqual("No temperature mentioned", normalize_temperatures("No temperature mentioned"))
        self.assertEqual("100 degrees", normalize_temperatures("100 degrees"))  # No F or C
        self.assertEqual("350°F and 180°C", normalize_temperatures("350 degrees F and 180 degrees C"))  # Both should be normalized

    def test_partial_matches(self):
        self.assertEqual("100 degrees Fahrenheit", normalize_temperatures("100 degrees Fahrenheit"))  # F not followed by a space or end of string, so no change
        self.assertEqual("100 degrees Celcius", normalize_temperatures("100 degrees Celcius"))  # Misspelled "Celsius", so no change

    def test_edge_cases(self):
        self.assertEqual("0°F", normalize_temperatures("0 degrees F"))  # Edge case with 0 degrees
        self.assertEqual("-10°C", normalize_temperatures("-10 degrees C"))  # Edge case with negative temperature


if __name__ == '__main__':
    unittest.main()
