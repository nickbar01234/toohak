import sys
import time
import random
import pygame as pg
import pyperclip
from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE
from . import utils
from ..type.aliases import *
from ..serializable import serializer as s


class MonitorScene(AbstractScene):
    def start_scene(self):
        self.leadersboard: LeadersBoard = []

        while True:
            for event in pg.event.get():
                self.handle_quit(event)

                # self.leadersboard = s.decode_leadersboard()
                # match event.type:
                #     case pg.MOUSEBUTTONDOWN:
                #         if self.submit_box.collidepoint(event.pos):
                #             self.__submit()
                #             return SceneState.REFEREE_MONITOR

            self.get_screen().fill("red")
            # utils.draw_submit_box(
            #     self.get_screen(), "lightblue", self.submit_box)
            pg.display.flip()
            time.sleep(3)
