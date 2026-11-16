"""Tests for Gymkhana's pure reward calculation service."""
import unittest

from KDF.Derby_Event.gymkhana_stampede.rewards import calculate_reward_total


class RewardCalculationTests(unittest.TestCase):
    def test_valid_checkpoint_adds_event_points(self):
        self.assertEqual(calculate_reward_total(25, 10, True), 35)

    def test_invalid_checkpoint_does_not_award_points(self):
        self.assertEqual(calculate_reward_total(25, 10, False), 25)

    def test_zero_value_event_does_not_change_total(self):
        self.assertEqual(calculate_reward_total(25, 0, True), 25)

    def test_negative_historic_totals_are_not_rewritten(self):
        self.assertEqual(calculate_reward_total(-5, 10, False), -5)

    def test_function_does_not_mutate_input_values(self):
        current = 10
        points = 5
        result = calculate_reward_total(current, points, True)
        self.assertEqual((current, points, result), (10, 5, 15))


if __name__ == "__main__":
    unittest.main(verbosity=2)
