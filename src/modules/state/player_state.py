from datetime import datetime
import threading
from enum import Enum, auto
import logging
from .client_state import ClientState
from ..type.aliases import *


class PlayerState(ClientState):
    def __init__(self):
        super().__init__()
        self.__init_time = None
        self.__progress: PlayerProgress = []

        self.game_starts = threading.Semaphore(0)
        self.__is_player = True

    # TODO: if we are just showing the leaderboard, are these functions still necessary?
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
