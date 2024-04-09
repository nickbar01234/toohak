import sys
import pygame
from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE


class RoleSelectionScene(AbstractScene):
    def start_scene(self):
        referee_box = self.__create_role_choice(0)
        player_box = self.__create_role_choice(100)

        referee_box_highlight = False
        player_box_highlight = False
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

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
                    # TODO(nickbar01234) - Handle sending information
                    return SceneState.QUIT

                if event.type == pygame.MOUSEBUTTONDOWN and player_box[0].collidepoint(event.pos):
                    # TODO(nickbar01234) - Handle sending information
                    return SceneState.PLAYER_QUESTION

            self.get_screen().fill("white")

            self.__create_prompt()

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

    def __create_prompt(self):
        font = STYLE["font"]["title"]
        text = font.render("Choose your role:", True, "black")
        rect = text.get_rect()
        rect.center = self.get_screen().get_rect().center
        rect.y = self.get_screen().get_height() // 4
        self.get_screen().blit(text, rect)

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