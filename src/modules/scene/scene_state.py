from enum import Enum, auto


class SceneState(Enum):
    ENTRY = auto()  # Role selection: player or referee

    PLAYER_WAITING = auto()  # Player's waiting room to start the game
    PLAYER_QUESTION = auto()  # Quiz in progress
    PLAYER_END = auto()  # Final result

    QUIT = auto()
