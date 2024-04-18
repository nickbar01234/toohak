import logging
import threading
import pygame as pg

from modules.network.network import Network
from modules.state.player_state import PlayerState

from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE

logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


class WaitScene(AbstractScene):
    def __init__(self, screen: pg.Surface, player_state: PlayerState, network: Network, text: str, next_state: SceneState, barrier: threading.Semaphore):
        super().__init__(screen, player_state, network)
        self.text = text
        self.next_state = next_state
        self.barrier = barrier

    def start_scene(self):
        self.get_screen().fill("white")

        textbox, textbox_border = self.get_utils().create_textbox()
        pg.draw.rect(self.get_screen(), "black", textbox_border)
        pg.draw.rect(self.get_screen(), "white", textbox)

        padding_x, padding_y = 10, 12
        text_surface = STYLE["font"]["text"].render(self.text, True, (0, 0, 0))
        # TODO(nickbar01234) - Handle clip text
        self.get_screen().blit(text_surface, (textbox.x + padding_x,
                                              textbox.y + textbox.height // 2 - padding_y))
        pg.display.flip()

        logger.info("Acquiring lock to to start game")
        self.barrier.acquire()
        logger.info("Successfully acquired lock to start game")

        return self.next_state
