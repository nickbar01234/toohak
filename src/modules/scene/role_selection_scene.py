import pygame
from .abstract_scene import AbstractScene
from .scene_state import SceneState, PLAYER_MODE, REFEREE_MODE
from .styles import STYLE
from . import utils


class RoleSelectionScene(AbstractScene):
    def start_scene(self):
        referee_box = self.__create_role_choice(0)
        player_box = self.__create_role_choice(100)

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
                    # inform server of client type
                    print("Client selected Player mode, informing server")
                    self.get_network().send_mode(PLAYER_MODE)
                    print("Sent to server")
                    return SceneState.REFEREE_ADD_QUESTION

                if event.type == pygame.MOUSEBUTTONDOWN and player_box[0].collidepoint(event.pos):
                    # inform server of client type
                    print("Client selected Referee mode, informing server")
                    self.get_network().send_mode(REFEREE_MODE)
                    print("Sent to server")
                    return SceneState.PLAYER_NAME

            self.get_screen().fill("white")

            utils.create_prompt(self.get_screen(
            ), "Choose your role:", (0, self.get_screen().get_height() // 4))

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

    def __create_role_choice(self, margin_y: int):
        border = 3
        width, height = 512, 64
        center_x, center_y = self.get_screen().get_rect().center
        textbox_border = pygame.Rect(0, 0, width, height)
        textbox_border.center = (center_x, center_y)
        textbox_border = textbox_border.move(0, margin_y)
        left_x, left_y = textbox_border.topleft
        textbox = pygame.Rect(0, 0, width - border * 2, height - border * 2)
        textbox.topleft = (left_x + border, left_y + border)

        return textbox, textbox_border
