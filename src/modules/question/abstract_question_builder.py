from abc import ABC, abstractmethod
from ..solution.type.abstract_solution import AbstractSolution
from .type.abstract_question import AbstractQuestion


class AbstractQuestionBuilder(ABC):
    @abstractmethod
    def add_question(self, question: str) -> "AbstractQuestionBuilder":
        '''
        Add question to the builder.
        '''

    @abstractmethod
    def remove_question(self) -> "AbstractQuestionBuilder":
        '''
        Remove question from the builder.
        '''

    @abstractmethod
    def add_option(self, option: str) -> "AbstractQuestionBuilder":
        '''
        Add an option to display to the builder.
        '''

    @abstractmethod
    def remove_option(self, option: str) -> "AbstractQuestionBuilder":
        '''
        Remove an option to display from the builder.
        '''

    @abstractmethod
    def add_solution(self, solution: AbstractSolution) -> "AbstractQuestionBuilder":
        '''
        Add a solution to the builder.
        '''

    @abstractmethod
    def remove_solution(self) -> "AbstractQuestionBuilder":
        '''
        Remove the solution from the builder.
        '''

    @abstractmethod
    def build(self) -> AbstractQuestion:
        '''
        Create a abstract question instance.
        '''
