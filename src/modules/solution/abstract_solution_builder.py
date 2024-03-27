from abc import ABC, abstractmethod
from .type import AbstractSolution


class AbstractSolutionBuilder(ABC):
    @abstractmethod
    def add_solution(self, option) -> "AbstractSolutionBuilder":
        '''
        Add a solution option to instance.
        '''

    @abstractmethod
    def remove_solution(self, option) -> "AbstractSolutionBuilder":
        '''
        Remove a solution option from instance.
        '''

    @abstractmethod
    def build(self) -> AbstractSolution:
        '''
        Build a solution instance
        '''
