import pickle
from .abstract_question import AbstractQuestion
from ... import AbstractSolution


class MultipleChoiceQuestion(AbstractQuestion):
    def __init__(self, question: str, solution: AbstractSolution, options: set[str]):
        super().__init__(question, solution)
        self.__options = options

    def __eq__(self, other):
        return isinstance(other, MultipleChoiceQuestion) and \
            self.get_question() == other.get_question() and \
            self.get_options() == other.get_options() and \
            self.verify(other.get_solution())

    def verify(self, solution):
        return self.get_solution().verify(solution)

    def draw(self, game):
        return

    def serialize(self):
        return pickle.dumps(self)

    def get_options(self):
        return self.__options
