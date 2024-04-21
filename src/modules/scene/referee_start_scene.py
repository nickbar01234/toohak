import pygame as pg
from .abstract_scene import AbstractScene
from .styles import STYLE
from .scene_state import SceneState


class RefreeStartScene(AbstractScene):
    def start_scene(self):
        start_box, start_box_border = self.get_utils().create_button((0, 0))

        while True:
            for event in pg.event.get():
                self.handle_quit(event)

                if event.type == pg.MOUSEBUTTONDOWN and start_box.collidepoint(event.pos):
                    self.get_network().send_signal_start_game()
                    self.get_player_state().player_start_barrier.release()
                    return SceneState.REFEREE_MONITOR

            self.get_screen().fill("white")
            self.get_utils().create_prompt(
                "Are you ready?", (0, self.get_screen().get_height() // 4))

            pg.draw.rect(self.get_screen(), "black", start_box_border)
            pg.draw.rect(self.get_screen(), "white", start_box)
            text = STYLE["font"]["question"].render(
                "Start game", True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = start_box.center
            self.get_screen().blit(text, text_rect)
            pg.display.flip()
