import unittest
import djg
from random import Random
from unittest.mock import patch


class TestNumberGeneration(unittest.TestCase):
    def setUp(self) -> None:
        self.random = Random(666)

    @patch("djg.random")
    def test_number(self, mock_random):
        djg.random.randrange._mock_side_effect = self.random.randrange
        number = djg._gen_number(minimum=0, maximum=10)
        self.assertEqual(number, 7)

    def test_number_bounds(self):
        number = djg._gen_number(minimum=0, maximum=10)
        self.assertGreaterEqual(number, 0)
        self.assertLessEqual(number, 10)

    @patch("djg.random")
    def test_number_multiple_of(self, mock_random):
        djg.random.randrange._mock_side_effect = self.random.randrange
        multiple_of = 17
        number = djg._gen_number(minimum=0, maximum=100, multiple_of=multiple_of)
        self.assertEqual(number, 68)
        self.assertEqual(number % multiple_of, 0)


class TestStringGeneration(unittest.TestCase):
    def test_str_bounds(self):
        length = len(djg._gen_str())
        self.assertGreaterEqual(length, 1)
        self.assertLessEqual(length, 10)

    def test_ignore_min_max(self):
        length = len(djg._gen_str(pattern=r"[a-z]{15,20}", min_length=5, max_length=10))
        self.assertGreater(length, 10)

