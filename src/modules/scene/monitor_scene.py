import sys
import time
import random
import pygame as pg
import pyperclip
from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE


class MonitorScene(AbstractScene):
    def start_scene(self):
        while True:
            for event in pg.event.get():
                self.handle_quit(event)
                # match event.type:
                #     case pg.MOUSEBUTTONDOWN:
                #         if self.submit_box.collidepoint(event.pos):
                #             self.__submit()
                #             return SceneState.REFEREE_MONITOR

            self.get_screen().fill("red")
            pg.display.flip()
            time.sleep(3)
