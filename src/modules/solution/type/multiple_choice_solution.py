import pickle
from .abstract_solution import AbstractSolution


class MultipleChoiceSolution(AbstractSolution):
    def __init__(self, solution: list[str]):
        super().__init__(sorted(solution))

    def verify(self, solution):
        return isinstance(solution, MultipleChoiceSolution) and self.get_solution() == solution.get_solution()

    def serialize(self):
        return pickle.dumps(self)

    # this solution builder is for user's answer
    def draw(self):
        # should have access to player's set of selections
        # solution_builder.add_solution("a")
        return
