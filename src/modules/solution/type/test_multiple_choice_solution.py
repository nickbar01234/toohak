import unittest
from .multiple_choice_solution import MultipleChoiceSolution


class TestMultipleChoiceSolution(unittest.TestCase):
    SOLUTION = ["D", "A", "B", "C"]

    def test_solution_is_sorted(self):
        self.assertListEqual(MultipleChoiceSolution(
            self.SOLUTION).get_solution(), ["A", "B", "C", "D"])

    def test_verify_correct_solution(self):
        gt = MultipleChoiceSolution(self.SOLUTION)
        answer = MultipleChoiceSolution(self.SOLUTION)
        self.assertTrue(gt.verify(answer))

    def test_verify_incorrect_solution(self):
        gt = MultipleChoiceSolution(self.SOLUTION)
        answer = MultipleChoiceSolution(["incorrect answer"])
        self.assertFalse(gt.verify(answer))

    def test_solution_serialize(self):
        self.assertEqual(MultipleChoiceSolution(
            self.SOLUTION).serialize(), "['A', 'B', 'C', 'D']")
