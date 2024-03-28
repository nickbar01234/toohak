from abc import abstractmethod
import pygame
from ...serializable.abstract_serializable import AbstractSerializable
from ... import AbstractSolution


class AbstractQuestion(AbstractSerializable):
    def __init__(self, question: str, solution: AbstractSolution):
        self.__question = question
        self.__solution = solution

    @abstractmethod
    def verify(self, solution: AbstractSolution):
        '''
        Given a solution instance, verify if the solution is correct.
        '''

    @abstractmethod
    def draw(self, game: pygame):
        '''
        Given a pygame instance, represent the question on the canvas.
        '''

    @abstractmethod
    def serialize(self) -> bytes:
        '''
        Convert instance to bytecode.
        '''

    def get_question(self):
        return self.__question

    def get_solution(self):
        return self.__solution
