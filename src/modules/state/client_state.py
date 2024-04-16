from datetime import datetime
import threading
from enum import Enum, auto
import logging
from ..type.aliases import *


class GameState(Enum):
    WAIT = auto()
    START = auto()
    END = auto()


class ClientState():
    def __init__(self):
        # logger setup
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

        self.__name = None
        self.__questions: list[Question] = []
        self.__leadersboard: LeadersBoard = []
        self.__leadersboard_lock = threading.Lock()

        self.start_barrier = threading.Semaphore(0)
        self.role_selection_barrier = threading.Semaphore(0)

        self.__game_state = GameState.START
        self.__is_player = None

    def get_name(self):
        return self.__name

    def set_name(self, name: Name):
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
        self.logger.info(
            "Received questions and updated the local question bank.")

    def get_leadersboard(self) -> LeadersBoard:
        with self.__leadersboard_lock:
            return list(self.__leadersboard)

    def set_leadersboard(self, leadersboard: LeadersBoard):
        with self.__leadersboard_lock:
            self.__leadersboard = leadersboard
            self.logger.debug("Set leadersboard: %s", self.__leadersboard)

    def game_ends(self):
        return self.__game_state == GameState.END

    def set_game_ends(self):
        self.__game_state = GameState.END

    def get_is_player(self):
        return self.__is_player

    def set_is_player(self, is_player: bool):
        self.__is_player = is_player
