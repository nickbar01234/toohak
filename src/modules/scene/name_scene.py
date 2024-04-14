import sys
import pygame
import pyperclip
import threading
from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE
from . import utils


class NameScene(AbstractScene):
    def __init__(self, screen, state, network, player_start_barrier: threading.Semaphore):
        super().__init__(screen, state, network)
        self.__player_start_barrier = player_start_barrier

    def start_scene(self):
        # TODO(nickbar01234) - Need to extract into a input class
        clock = pygame.time.Clock()
        name = ""
        active = False
        while True:
            textbox, textbox_border = utils.create_textbox(self.get_screen())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    active = textbox.collidepoint(event.pos)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.get_network().send_name(name)
                        self.__player_start_barrier.release()
                        return SceneState.PLAYER_WAIT
                    elif event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL or event.mod & pygame.KMOD_META):
                        name = pyperclip.paste()
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

            self.get_screen().fill("white")

            utils.create_prompt(self.get_screen(),
                                "Enter your name:", (0, 128))

            pygame.draw.rect(self.get_screen(), pygame.Color(
                "#8489FBFF") if active else "black", textbox_border)
            pygame.draw.rect(self.get_screen(), "white", textbox)

            padding_x, padding_y = 10, 12
            text_surface = STYLE["font"]["text"].render(name, True, (0, 0, 0))
            # TODO(nickbar01234) - Handle clip text
            self.get_screen().blit(text_surface, (textbox.x + padding_x,
                                                  textbox.y + textbox.height // 2 - padding_y))
            pygame.display.flip()

            clock.tick(STYLE["fps"])
