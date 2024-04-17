from enum import Enum, auto


class SceneState(Enum):
    ENTRY = auto()  # Setup server IP address

    ROLE_SELECTION = auto()

    PLAYER_WAIT = auto()  # Player's waiting room
    PLAYER_NAME = auto()  # Player's entering name
    PLAYER_QUESTION = auto()  # Quiz in progress
    PLAYER_END = auto()  # Final result

    # Referee chooses whether to use default question sets or define their own
    REFEREE_CHOOSE_QUESTION_SET = auto()
    REFEREE_ADD_QUESTION = auto()  # Referee adds questions to question bank
    REFEREE_START_SCENE = auto()
    REFEREE_MONITOR = auto()  # Referee's view

    QUIT = auto()


FINISHED_ROLE_SELECTION = (SceneState.PLAYER_NAME,
                           SceneState.REFEREE_ADD_QUESTION)
