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
            self.logger.debug(f"Received leadersboard {
                              self.get_player_state().get_leadersboard()}")

            text_surface = STYLE["font"]["title"].render(
                "Monitoring Leaderboard...", True, (0, 0, 0))
            screen_midtop = self.get_screen().get_rect().midtop
            text_rect = text_surface.get_rect(
                midtop=(screen_midtop[0], screen_midtop[1] + 200))
            self.get_screen().blit(text_surface, text_rect)

            utils.draw_leadersboard(
                self.get_screen(), self.get_player_state().get_leadersboard(), text_rect)
            pg.display.flip()
