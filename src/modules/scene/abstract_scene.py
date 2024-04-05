from abc import ABC, abstractmethod
from pygame import Surface
from ..state import PlayerState

# Join game scene
# Referee or Player scene
# Player: Answering question, Final game results
# [-join-][-wait-][----------game----------][-end-]


class AbstractScene(ABC):
    def __init__(self, screen: Surface, player_state: PlayerState):
        self.__screen = screen
        self.__player_state = player_state

    @abstractmethod
    def start_scene(self):
        '''
        Runs a scene and return a enum to transition to the next scene.
        '''
