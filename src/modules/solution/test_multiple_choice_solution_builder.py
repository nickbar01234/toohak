import unittest
from .multiple_choice_solution_builder import MultipleChoiceSolutionBuilder


class TestMultipleChoiceSolutionBuilder(unittest.TestCase):
    def test_add_choice(self):
        self.assertListEqual(MultipleChoiceSolutionBuilder().add_solution(
            "B").add_solution("A").build().get_solution(), ["A", "B"])

    def test_remove_solution(self):
        solution = MultipleChoiceSolutionBuilder().add_solution(
            "A").add_solution("B").remove_solution("A").build()
        self.assertListEqual(solution.get_solution(), ["B"])
