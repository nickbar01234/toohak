from datetime import datetime
from ..question.type.abstract_question import AbstractQuestion
from ..serializable import serializer as s

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

from enum import Enum, auto

class GameState(Enum):
    START = auto()
    END = auto()

class PlayerState:
    def __init__(self, network):
        # TODO - Change type hint for network
        self.__network = network
        self.__name = None
        self.__questions = []
        self.__progress = []
        self.__init_time = None
        self.__leadersboard = []
        self.__game_state = GameState.START

    def get_name(self):
        return self.__name

    def set_name(self, name: str):
        # TODO - Send server
        if not isinstance(name, str):
            raise RuntimeError(
                f"Expect name to be of type str, but received type {type(name)}")

        self.__name = name

    def get_questions(self):
        return self.__questions

    def set_questions(self, questions: list[AbstractQuestion]):
        if not isinstance(questions, list):
            raise RuntimeError(
                f"Expect name to be of type list, but received type {type(questions)}")

        self.__questions = questions

    def get_progress(self):
        return self.__progress

    def set_progress(self, correctness):
        # TODO - Send server
        if not isinstance(correctness, bool):
            raise RuntimeError(
                f"Expect name to be of type boolean, but received type {type(correctness)}")

        self.__progress.append(correctness)

    def get_init_time(self):
        return self.__init_time

    def set_init_time(self):
        self.__init_time = datetime.now()

    def get_leadersboard(self):
        return self.__leadersboard
    
    def set_leadersboard(self, leadersboard):
        self.__leadersboard = leadersboard
    
    def game_ends(self):
        return self.__game_state == GameState.END
    
    def set_game_ends(self):
        self.__game_state = GameState.END


