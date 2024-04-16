from abc import ABC, abstractmethod
import sys
import pygame as pg
from ..state import ClientState
from ..network.network import Network


class AbstractScene(ABC):
    def __init__(self, screen: pg.Surface, client_state: ClientState, network: Network):
        self.__screen = screen
        self.__client_state = client_state
        self.__network = network

    @abstractmethod
    def start_scene(self):
        '''
        Runs a scene and return a enum to transition to the next scene.
        '''

    def get_screen(self):
        return self.__screen

    def get_client_state(self):
        return self.__client_state

    def get_network(self):
        return self.__network

    def handle_quit(self, event: pg.event):
        match event.type:
            case pg.QUIT:
                self.get_network().disconnect()
                pg.quit()
                sys.exit(0)
