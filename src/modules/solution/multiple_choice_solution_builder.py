from .abstract_solution_builder import AbstractSolutionBuilder
from .type import MultipleChoiceSolution


class MultipleChoiceSolutionBuilder(AbstractSolutionBuilder):
    def __init__(self):
        super().__init__()
        self.__solutions = set()

    def add_solution(self, option):
        self.__solutions.add(option)
        return self

    def remove_solution(self, option):
        self.__solutions.remove(option)
        return self

    def build(self):
        return MultipleChoiceSolution(list(self.__solutions))
