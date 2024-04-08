from .abstract_solution_builder import AbstractSolutionBuilder
from .type import MultipleChoiceSolution


class MultipleChoiceSolutionBuilder(AbstractSolutionBuilder):
    def __init__(self, solutions: set = None):
        super().__init__()
        self.__solutions = solutions if solutions else set()

    def add_solution(self, option):
        self.__solutions.add(option)
        return self

    def remove_solution(self, option):
        self.__solutions.remove(option)
        return self

    def add_solutions(self, options):
        for option in options:
            self.__solutions.add(option)
        return self

    def remove_solutions(self, options):
        for option in options:
            self.__solutions.remove(option)
        return self

    def build(self):
        return MultipleChoiceSolution(list(self.__solutions))
