import time
import pygame as pg
from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE


class RoleSelectionScene(AbstractScene):
    def start_scene(self):
        referee_box = self.get_utils().create_button((0, 0))
        player_box = self.get_utils().create_button((0, 100))

        referee_box_highlight = False
        player_box_highlight = False
        while True:

            for event in pg.event.get():
                self.handle_quit(event)

                if referee_box[0].collidepoint(pg.mouse.get_pos()):
                    referee_box_highlight = True
                    player_box_highlight = False
                elif player_box[0].collidepoint(pg.mouse.get_pos()):
                    player_box_highlight = True
                    referee_box_highlight = False
                else:
                    referee_box_highlight = False
                    player_box_highlight = False

                if event.type == pg.MOUSEBUTTONDOWN and referee_box[0].collidepoint(event.pos):
                    # auto-select player if referee is selected by another player
                    print("Receiving role selection response")
                    status = self.get_network().send_role("referee")
                    print(f"STATUS is {status}")
                    if status:
                        return self.select_referee()
                    else:
                        self.display_bad_selection_msg()
                        return self.select_player()

                if event.type == pg.MOUSEBUTTONDOWN and player_box[0].collidepoint(event.pos):
                    self.get_network().send_role("player")
                    return self.select_player()

            self.get_screen().fill("white")

            self.get_utils().create_prompt(
                "Choose your role:", (0, self.get_screen().get_height() // 4))

            for (box, border), content, highlight in zip([referee_box, player_box], ["Refree", "Player"], [referee_box_highlight, player_box_highlight]):
                pg.draw.rect(self.get_screen(), pg.Color(
                    "#8489FBFF" if highlight else "black"), border)
                pg.draw.rect(self.get_screen(), "white", box)
                text = STYLE["font"]["question"].render(
                    content, True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.center = box.center
                self.get_screen().blit(text, text_rect)

            pg.display.flip()

    def select_player(self):
        self.get_player_state().set_is_player(True)
        self.get_player_state().role_selection_barrier.release()
        print("ROLE SELECTION: PLAYER")
        return SceneState.PLAYER_NAME

    def select_referee(self):
        self.get_player_state().set_is_player(False)
        self.get_player_state().role_selection_barrier.release()

        return SceneState.REFEREE_CHOOSE_QUESTION_SET


    def display_bad_selection_msg(self):
        self.get_screen().fill("beige")
        text_surface = STYLE["font"]["question"].render(
            "Referee has already been selected, you will be a player instead!", True, (0, 0, 0))
        text_rect = text_surface.get_rect(
            center=self.get_screen().get_rect().center)
        self.get_screen().blit(text_surface, text_rect)
        pg.display.flip()
        time.sleep(2)
