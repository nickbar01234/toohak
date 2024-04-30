import pygame as pg
from .abstract_scene import AbstractScene
from .styles import STYLE
from .scene_state import SceneState


class MonitorScene(AbstractScene):
    def start_scene(self):
        while not self.get_player_state().is_game_end:
            for event in pg.event.get():
                self.handle_quit(event)

            # render graphics
            self.get_screen().fill("lightgreen")
            text_surface = STYLE["font"]["title"].render(
                "Monitoring Leaderboard...", True, (0, 0, 0))
            screen_midtop = self.get_screen().get_rect().midtop
            text_rect = text_surface.get_rect(
                midtop=(screen_midtop[0], screen_midtop[1] + 100))
            self.get_screen().blit(text_surface, text_rect)

            leaderboard_box = self.get_utils().create_leaderboard_box(fromtop=150)
            self.get_utils().draw_leaderboard(leaderboard_box, len(self.get_player_state().get_questions()),
                                              self.get_player_state().get_leadersboard(), display_correctness=True)
            pg.display.flip()

        return SceneState.QUIT
