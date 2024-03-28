import unittest
from .multiple_choice_question_builder import MultipleQuestionBuilder
from .type import MultipleChoiceQuestion
from .. import MultipleChoiceSolutionBuilder


class TestMultipleChoiceQuestionBuilder(unittest.TestCase):
    def test_build_question(self):
        q1 = MultipleQuestionBuilder().add_question(
            "foo").add_option("1").add_solution(MultipleChoiceSolutionBuilder().add_solution("1").build()).build()
        q2 = MultipleChoiceQuestion(
            "foo", MultipleChoiceSolutionBuilder().add_solution("1").build(), set(["1"]))
        self.assertEqual(q1, q2)

    def test_missing_kwargs_throw_error(self):
        self.assertRaises(Exception, MultipleQuestionBuilder().build)
