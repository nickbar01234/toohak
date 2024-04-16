from enum import Enum, auto


class SceneState(Enum):
    # Entry states
    ENTRY = auto()  # Setup server IP address
    ROLE_SELECTION = auto()
    NAME = auto()  # Player's entering name

    # Player states
    PLAYER_WAIT = auto()  # Player's waiting room
    PLAYER_QUESTION = auto()  # Quiz in progress
    PLAYER_END = auto()  # Final result

    # Referee states
    REFEREE_ADD_QUESTION = auto()  # Referee adds questions to question bank
    REFEREE_START_SCENE = auto()
    REFEREE_MONITOR = auto()  # Referee's view

    # Quit states
    QUIT = auto()
