import pickle
from .abstract_question import AbstractQuestion
from ...solution.type import AbstractSolution
from ...scene.styles import STYLE


class MultipleChoiceQuestion(AbstractQuestion):
    def __init__(self, question: str, solution: AbstractSolution, options: set[str]):
        super().__init__(question, solution, options)

    def __eq__(self, other):
        return isinstance(other, MultipleChoiceQuestion) and \
            self.get_question() == other.get_question() and \
            self.get_options() == other.get_options() and \
            self.verify(other.get_solution())

    def verify(self, solution):
        return self.get_solution().verify(solution)

    def draw(self, screen):
        font = STYLE["font"]["question"]
        text = font.render(self.get_question(), True, (0, 0, 0))
        rect = text.get_rect()
        rect.midtop = screen.get_rect().midtop
        rect = rect.inflate(0, -50)
        screen.blit(text, rect)

    def serialize(self):
        return pickle.dumps(self)
