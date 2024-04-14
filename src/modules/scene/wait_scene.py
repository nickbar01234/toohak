import threading
import pygame as pg
from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE
from . import utils


class WaitScene(AbstractScene):
    def start_scene(self):
        self.get_screen().fill("white")

        textbox, textbox_border = utils.create_textbox(self.get_screen())
        pg.draw.rect(self.get_screen(), "lightgreen", textbox)
        padding_x, padding_y = 10, 12
        text_surface = STYLE["font"]["text"].render(
            "You're in! We're waiting for other players to get ready...", True, (0, 0, 0))
        # TODO(nickbar01234) - Handle clip text
        self.get_screen().blit(text_surface, (textbox.x + padding_x,
                                              textbox.y + textbox.height // 2 - padding_y))
        pg.display.flip()

        return SceneState.PLAYER_QUESTION
