from abc import ABC, abstractmethod
from pygame import Surface, Rect
from ...solution import AbstractSolution


class AbstractQuestion(ABC):
    def __init__(self, question: str, solution: AbstractSolution, options: list[str]):
        self.__question = question
        self.__solution = solution
        self.__options = options

    @abstractmethod
    def verify(self, solution: AbstractSolution):
        '''
        Given a solution instance, verify if the solution is correct.
        '''

    @abstractmethod
    def draw(self, screen: Surface) -> Rect:
        '''
        Given a pygame instance, represent the question on the canvas.
        '''

    def get_question(self):
        return self.__question

    def get_solution(self):
        return self.__solution

    def get_options(self):
        return self.__options
