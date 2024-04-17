import pygame
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

            for event in pygame.event.get():
                self.handle_quit(event)

                if referee_box[0].collidepoint(pygame.mouse.get_pos()):
                    referee_box_highlight = True
                    player_box_highlight = False
                elif player_box[0].collidepoint(pygame.mouse.get_pos()):
                    player_box_highlight = True
                    referee_box_highlight = False
                else:
                    referee_box_highlight = False
                    player_box_highlight = False

                if event.type == pygame.MOUSEBUTTONDOWN and referee_box[0].collidepoint(event.pos):
                    self.get_network().send_role("referee")
                    self.get_player_state().set_is_player(False)
                    self.get_player_state().role_selection_barrier.release()
                    return SceneState.REFEREE_ADD_QUESTION

                if event.type == pygame.MOUSEBUTTONDOWN and player_box[0].collidepoint(event.pos):
                    self.get_network().send_role("player")
                    self.get_player_state().set_is_player(True)
                    self.get_player_state().role_selection_barrier.release()
                    return SceneState.PLAYER_NAME

            self.get_screen().fill("white")

            self.get_utils().create_prompt(
                "Choose your role:", (0, self.get_screen().get_height() // 4))

            for (box, border), content, highlight in zip([referee_box, player_box], ["Refree", "Player"], [referee_box_highlight, player_box_highlight]):
                pygame.draw.rect(self.get_screen(), pygame.Color(
                    "#8489FBFF" if highlight else "black"), border)
                pygame.draw.rect(self.get_screen(), "white", box)
                text = STYLE["font"]["question"].render(
                    content, True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.center = box.center
                self.get_screen().blit(text, text_rect)

            pygame.display.flip()
