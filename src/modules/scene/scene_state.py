from enum import Enum, auto


class SceneState(Enum):
    ENTRY = auto()  # Setup server IP address

    ROLE_SELECTION = auto()

    PLAYER_WAITING = auto()  # Player's waiting room to start the game
    PLAYER_NAME = auto()  # Player's entering name
    PLAYER_QUESTION = auto()  # Quiz in progress
    PLAYER_END = auto()  # Final result

    QUIT = auto()
