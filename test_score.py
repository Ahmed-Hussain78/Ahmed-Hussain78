"""Unit tests for score.py MCQ scoring utility."""

import unittest
from score import calculate_score, format_summary


class TestCalculateScore(unittest.TestCase):

    def test_basic_no_negatives(self):
        result = calculate_score(33, 5)
        self.assertEqual(result["correct"], 33)
        self.assertEqual(result["wrong"], 5)
        self.assertEqual(result["total"], 38)
        self.assertEqual(result["skipped"], 0)
        self.assertAlmostEqual(result["raw_marks"], 33.0)
        self.assertAlmostEqual(result["penalty"], 0.0)
        self.assertAlmostEqual(result["final_marks"], 33.0)
        self.assertAlmostEqual(result["percentage"], 33 / 38 * 100)

    def test_explicit_total_with_skipped(self):
        result = calculate_score(33, 5, total=40)
        self.assertEqual(result["total"], 40)
        self.assertEqual(result["skipped"], 2)
        self.assertAlmostEqual(result["percentage"], 33 / 40 * 100)

    def test_negative_marking(self):
        result = calculate_score(33, 5, total=38, negative=0.25)
        self.assertAlmostEqual(result["penalty"], 1.25)
        self.assertAlmostEqual(result["final_marks"], 31.75)
        self.assertAlmostEqual(result["percentage"], 31.75 / 38 * 100)

    def test_all_correct(self):
        result = calculate_score(10, 0, total=10)
        self.assertAlmostEqual(result["final_marks"], 10.0)
        self.assertAlmostEqual(result["percentage"], 100.0)

    def test_all_wrong(self):
        result = calculate_score(0, 10, total=10, negative=0.25)
        self.assertAlmostEqual(result["final_marks"], -2.5)
        self.assertAlmostEqual(result["percentage"], -25.0)

    def test_zero_questions(self):
        result = calculate_score(0, 0)
        self.assertEqual(result["total"], 0)
        self.assertAlmostEqual(result["percentage"], 0.0)

    def test_negative_correct_raises(self):
        with self.assertRaises(ValueError):
            calculate_score(-1, 5)

    def test_negative_wrong_raises(self):
        with self.assertRaises(ValueError):
            calculate_score(5, -1)

    def test_negative_penalty_raises(self):
        with self.assertRaises(ValueError):
            calculate_score(5, 3, negative=-0.5)

    def test_total_less_than_answered_raises(self):
        with self.assertRaises(ValueError):
            calculate_score(33, 5, total=30)

    def test_derived_total_no_skipped(self):
        result = calculate_score(7, 3)
        self.assertEqual(result["total"], 10)
        self.assertEqual(result["skipped"], 0)


class TestFormatSummary(unittest.TestCase):

    def test_summary_contains_key_fields(self):
        result = calculate_score(33, 5)
        summary = format_summary(result)
        self.assertIn("33", summary)
        self.assertIn("5", summary)
        self.assertIn("38", summary)
        self.assertIn("%", summary)

    def test_summary_shows_penalty_when_negative(self):
        result = calculate_score(33, 5, negative=0.25)
        summary = format_summary(result, negative=0.25)
        self.assertIn("Penalty", summary)
        self.assertIn("1.25", summary)

    def test_summary_no_penalty_line_when_zero(self):
        result = calculate_score(33, 5)
        summary = format_summary(result, negative=0.0)
        self.assertNotIn("Penalty", summary)


if __name__ == "__main__":
    unittest.main()
