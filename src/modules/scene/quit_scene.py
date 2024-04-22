import pygame as pg

from .abstract_scene import AbstractScene
from .styles import STYLE


class QuitScene(AbstractScene):
    def start_scene(self):

        button, button_border = self.get_utils().create_button((0, -100))
        while True:
            for event in pg.event.get():
                self.handle_quit(event)

                if event.type == pg.MOUSEBUTTONDOWN and button.collidepoint(event.pos):
                    self.handle_quit(pg.event.Event(pg.QUIT))

            self.get_screen().fill("white")

            # self.get_utils().draw_results(
            #     button_border, self.get_player_state().get_leadersboard(), len(self.get_player_state().get_questions()))

            self.get_utils().create_prompt("Thanks for playing!",
                                           (0, self.get_screen().get_height() // 8))

            pg.draw.rect(self.get_screen(), "black", button_border)
            pg.draw.rect(self.get_screen(), "white", button)

            quit_text = STYLE["font"]["question"].render(
                "Quit", True, (0, 0, 0))
            quit_rect = quit_text.get_rect()
            quit_rect.center = button.center
            self.get_screen().blit(quit_text, quit_rect)

            leaderboard_box = self.get_utils().create_leaderboard_box()
            leaderboard_box.top = quit_rect.bottom + 64
            self.get_utils().draw_leaderboard(leaderboard_box, len(self.get_player_state().get_questions()),
                                              self.get_player_state().get_leadersboard(), True)

            pg.display.flip()
