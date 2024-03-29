from abc import abstractmethod
from ...serializable.abstract_serializable import AbstractSerializable


class AbstractSolution(AbstractSerializable):
    def __init__(self, solution: any):
        self.__solution = solution

    @abstractmethod
    def verify(self, solution: "AbstractSolution") -> bool:
        '''
        Given a solution instance, compare if the solution is equal to self.
        '''

    @abstractmethod
    def serialize(self) -> str:
        '''
        Convert instance to bytecode.
        '''

    def get_solution(self):
        return self.__solution
