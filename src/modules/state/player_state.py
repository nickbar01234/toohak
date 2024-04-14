from datetime import datetime
import threading
from enum import Enum, auto
import logging
from ..serializable import serializer as s
from ..question.type.abstract_question import AbstractQuestion
from .server_state import ServerState
from ..type.aliases import *

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

        self.__questions: list[Question] = []
        self.__progress: PlayerProgress = []
        self.__init_time = None
        self.__leadersboard: LeadersBoard = []
        self.__leadersboard_lock = threading.Lock()

        self.__game_state = GameState.START
        self.game_starts = threading.Semaphore(0)

    def get_name(self):
        return self.__name

    def set_name(self, name: Name):
        # TODO - Send server
        if not isinstance(name, str):
            raise RuntimeError(
                f"Expect name to be of type str, but received type {type(name)}")

        self.__name = name

    def get_questions(self) -> list[Question]:
        return self.__questions

    def set_questions(self, questions: list[Question]):
        if not isinstance(questions, list):
            raise RuntimeError(
                f"Expect name to be of type list, but received type {type(questions)}")

        self.__questions = questions
        logger.info("Received questions and updated the local question bank.")

    def get_progress(self) -> PlayerProgress:
        return self.__progress

    def set_progress(self, correctness: bool):
        # TODO - Send server
        if not isinstance(correctness, bool):
            raise RuntimeError(
                f"Expect name to be of type boolean, but received type {type(correctness)}")

        self.__progress.append(correctness)

    def get_init_time(self):
        return self.__init_time

    def set_init_time(self):
        self.__init_time = datetime.now()

    def get_leadersboard(self) -> LeadersBoard:
        with self.__leadersboard_lock:
            return list(self.__leadersboard)

    def set_leadersboard(self, leadersboard: LeadersBoard):
        with self.__leadersboard_lock:
            self.__leadersboard = leadersboard
            logger.debug("Set leadersboard: %s", self.__leadersboard)

    def game_ends(self):
        return self.__game_state == GameState.END

    def set_game_ends(self):
        self.__game_state = GameState.END
