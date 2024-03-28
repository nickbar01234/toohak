import pickle
from .abstract_solution import AbstractSolution


class MultipleChoiceSolution(AbstractSolution):
    def __init__(self, solution: list[str]):
        super().__init__(sorted(solution))

    def verify(self, solution):
        return isinstance(solution, MultipleChoiceSolution) and self.get_solution() == solution.get_solution()

    def serialize(self):
        return pickle.dumps(self)

    def draw(self, game):
        return
