from datetime import datetime
import threading
from enum import Enum, auto
import logging
from .client_state import ClientState
from ..type.aliases import *


class RefereeState(ClientState):
    def __init__(self):
        self.__is_player = False
