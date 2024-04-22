from .abstract_question_builder import AbstractQuestionBuilder
from .type import MultipleChoiceQuestion


class MultipleChoiceQuestionBuilder(AbstractQuestionBuilder):
    def __init__(self):
        self.__kwargs = {}

    def add_question(self, question):
        self.__kwargs["question"] = question
        return self

    def remove_question(self):
        if "question" in self.__kwargs:
            del self.__kwargs["question"]
        return self

    def add_option(self, option):
        self.__kwargs.setdefault("options", []).append(option)
        return self

    def remove_option(self, option: str):
        self.__kwargs.setdefault("options", []).remove(option)
        return self

    def add_solution(self, solution):
        self.__kwargs["solution"] = solution
        return self

    def remove_solution(self):
        if "solution" in self.__kwargs:
            del self.__kwargs["solution"]

    def build(self):
        return MultipleChoiceQuestion(**self.__kwargs)
