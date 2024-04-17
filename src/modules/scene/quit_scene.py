import pygame as pg

from .abstract_scene import AbstractScene
from .styles import STYLE
from . import utils


class QuitScene(AbstractScene):
    def start_scene(self):

        button, button_border = utils.create_button(
            self.get_screen(), (0, -100))
        while True:
            for event in pg.event.get():
                self.handle_quit(event)

                if event.type == pg.MOUSEBUTTONDOWN and button.collidepoint(event.pos):
                    self.handle_quit(pg.event.Event(pg.QUIT))

            self.get_screen().fill("white")

            for idx, (name, n_questions) in enumerate(self.get_player_state().get_leadersboard()):
                text = STYLE["font"]["text"].render(
                    f"{name}: {n_questions}", True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.midtop = button_border.midbottom
                text_rect.top = button_border.bottom
                text_rect = text_rect.move(0, button_border.height + idx * 32)
                self.get_screen().blit(text, text_rect)

            utils.create_prompt(self.get_screen(
            ), "Thanks for playing!", (0, self.get_screen().get_height() // 8))

            pg.draw.rect(self.get_screen(), "black", button_border)
            pg.draw.rect(self.get_screen(), "white", button)

            quit_text = STYLE["font"]["question"].render(
                "Quit", True, (0, 0, 0))
            quit_rect = quit_text.get_rect()
            quit_rect.center = button.center
            self.get_screen().blit(quit_text, quit_rect)

            pg.display.flip()
