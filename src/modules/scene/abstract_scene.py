from abc import ABC, abstractmethod
from pygame import Surface
from ..state import PlayerState


class AbstractScene(ABC):
    def __init__(self, screen: Surface, player_state: PlayerState, network: any):
        self.__screen = screen
        self.__player_state = player_state
        self.__network = network

    @abstractmethod
    def start_scene(self):
        '''
        Runs a scene and return a enum to transition to the next scene.
        '''

    def get_screen(self):
        return self.__screen

    def get_player_state(self):
        return self.__player_state

    def get_network(self):
        return self.__network
