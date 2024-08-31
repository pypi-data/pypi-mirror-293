import unittest

from recipy.utils import parse_time


class TestParseTime(unittest.TestCase):
    def test_valid_iso_duration(self):
        self.assertEqual(150, parse_time("PT2H30M"))  # 2 hours and 30 minutes
        self.assertEqual(120, parse_time("PT2H"))  # 2 hours only
        self.assertEqual(45, parse_time("PT45M"))  # 45 minutes only
        self.assertEqual(0, parse_time("PT0H0M"))  # 0 hours and 0 minutes
        self.assertEqual(60, parse_time("PT1H"))  # 1 hour only

    def test_invalid_iso_duration(self):
        self.assertIsNone(parse_time("2H30M"))  # Missing 'PT' prefix
        self.assertIsNone(parse_time("PT2H30"))  # Missing 'M' after minutes
        self.assertIsNone(parse_time("PT2M30H"))  # Incorrect order
        self.assertIsNone(parse_time("P2H30M"))  # Incorrect prefix
        self.assertIsNone(parse_time("PT"))  # Incomplete duration

    def test_empty_or_whitespace_string(self):
        self.assertIsNone(parse_time(""))  # Empty string
        self.assertIsNone(parse_time("   "))  # Whitespace string

    def test_no_time_provided(self):
        self.assertIsNone(parse_time("PT"))  # 'PT' with no time should return 0

    def test_minutes_only(self):
        self.assertEqual(30, parse_time("PT30M"))  # 30 minutes only
        self.assertEqual(90, parse_time("PT1H30M"))  # 1 hour and 30 minutes
        self.assertEqual(1, parse_time("PT1M"))  # 1 minute only

    def test_hours_only(self):
        self.assertEqual(120, parse_time("PT2H"))  # 2 hours only
        self.assertEqual(300, parse_time("PT5H"))  # 5 hours only


if __name__ == '__main__':
    unittest.main()
