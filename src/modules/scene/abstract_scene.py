from abc import ABC, abstractmethod
import sys
import logging
import pygame as pg
from .utils import Utils
from ..state import PlayerState
from ..network.network import Network


class AbstractScene(ABC):
    def __init__(self, screen: pg.Surface, player_state: PlayerState, network: Network):
        self.__screen = screen
        self.__player_state = player_state
        self.__network = network
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
        self.__utils = Utils(self.__screen)

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

    def handle_quit(self, event: pg.event):
        match event.type:
            case pg.QUIT:
                self.get_network().disconnect()
                pg.quit()
                sys.exit(0)

    def get_utils(self):
        return self.__utils
