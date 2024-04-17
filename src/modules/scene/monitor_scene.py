import sys
import time
import random
import pygame as pg
import pyperclip
from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE
from . import utils


class MonitorScene(AbstractScene):
    def start_scene(self):
        while True:
            for event in pg.event.get():
                self.handle_quit(event)

            self.get_screen().fill("lightgreen")
            utils.draw_leadersboard(
                self.get_screen(), self.get_player_state().get_leadersboard(), self.get_screen().get_rect())
            pg.display.flip()
