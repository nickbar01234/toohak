import logging
import pygame as pg

from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE

logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


class WaitScene(AbstractScene):
    def start_scene(self):
        self.get_screen().fill("white")

        textbox, textbox_border = self.get_utils().create_textbox()
        pg.draw.rect(self.get_screen(), "black", textbox_border)
        pg.draw.rect(self.get_screen(), "white", textbox)

        padding_x, padding_y = 10, 12
        text_surface = STYLE["font"]["text"].render(
            "You're in! We're waiting for other players to get ready...", True, (0, 0, 0))
        # TODO(nickbar01234) - Handle clip text
        self.get_screen().blit(text_surface, (textbox.x + padding_x,
                                              textbox.y + textbox.height // 2 - padding_y))
        pg.display.flip()

        logger.info("Acquiring lock to start game")
        self.get_player_state().game_starts.acquire()
        logger.info("Successfully acquired lock to start game")

        return SceneState.PLAYER_QUESTION
