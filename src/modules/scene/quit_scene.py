import time
import sys
import pygame

from .abstract_scene import AbstractScene
from .styles import STYLE


class QuitScene(AbstractScene):
    def start_scene(self):
        text = STYLE["font"]["title"].render(
            "Thanks for playing!", True, (0, 0, 0))
        rect = text.get_rect()
        rect.center = self.get_screen().get_rect().center

        while True:
            for event in pygame.event.get():
                self.handle_quit(event)

            self.get_screen().fill("white")
            self.get_screen().blit(text, rect)
            pygame.display.flip()

            # TODO: Do something more interesting
            time.sleep(3)
            pygame.quit()
            sys.exit(0)
