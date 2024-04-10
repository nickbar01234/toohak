import logging
from ..serializable import serializer as s
from ..question.type.abstract_question import AbstractQuestion
from datetime import datetime
import threading
from enum import Enum, auto
<< << << < Updated upstream
== == == =
>>>>>> > Stashed changes

logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


class GameState(Enum):
    WAIT = auto()
    START = auto()
    END = auto()


class PlayerState:
    def __init__(self, network):
        # TODO - Change type hint for network
        self.__network = network
        self.__name = None

        self.__questions_lock = threading.Lock()
        self.__questions_condition = threading.Condition(self.__questions_lock)
        self.__questions = []
        self.__progress: list[bool] = []
        self.__init_time = None
        self.__leadersboard = []
        self.__leadersboardLock = threading.Lock()
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
        with self.__questions_lock:
            while len(self.__questions) == 0:
                self.__questions_condition.wait()
            return self.__questions

    def set_questions(self, questions: list[AbstractQuestion]):
        if not isinstance(questions, list):
            raise RuntimeError(
                f"Expect name to be of type list, but received type {type(questions)}")

        with self.__questions_lock:
            self.__questions = questions
            self.__questions_condition.notify()

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
        with self.__leadersboardLock:
            return self.__leadersboard

    def set_leadersboard(self, leadersboard):
        with self.__leadersboardLock:
            self.__leadersboard = leadersboard

    def game_ends(self):
        return self.__game_state == GameState.END

    def set_game_ends(self):
        self.__game_state = GameState.END
