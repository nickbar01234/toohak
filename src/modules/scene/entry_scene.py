import sys
import pygame
import pyperclip
from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE


class EntryScene(AbstractScene):
    def start_scene(self):
        clock = pygame.time.Clock()

        ip = ""

        active = False
        textbox, textbox_border = self.__create_textbox()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    active = textbox.collidepoint(event.pos)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.get_network().connect(ip)
                        return SceneState.PLAYER_QUESTION
                    elif event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL or event.mod & pygame.KMOD_META):
                        ip = pyperclip.paste()
                    elif event.key == pygame.K_BACKSPACE:
                        ip = ip[:-1]
                    else:
                        ip += event.unicode

            self.get_screen().fill("white")

            self.__create_prompt()

            pygame.draw.rect(self.get_screen(), pygame.Color(
                "#8489FBFF") if active else "black", textbox_border)
            pygame.draw.rect(self.get_screen(), "white", textbox)

            padding_x = 10
            text_surface = STYLE["font"]["text"].render(ip, True, (0, 0, 0))
            # TODO(nickbar01234) - Handle clip text
            self.get_screen().blit(text_surface, (textbox.x + padding_x,
                                                  textbox.y + textbox.height // 2 - 12))
            pygame.display.flip()

            clock.tick(STYLE["fps"])

    def __create_prompt(self):
        font = STYLE["font"]["title"]
        text = font.render("Enter server IP address:", True, "black")
        rect = text.get_rect()
        rect.center = self.get_screen().get_rect().center
        rect = rect.inflate(0, 256)
        self.get_screen().blit(text, rect)

    def __create_textbox(self):
        border = 3
        width, height = 512, 64
        center_x, center_y = self.get_screen().get_rect().center
        textbox_border = pygame.Rect(0, 0, width, height)
        textbox_border.center = (center_x, center_y)
        left_x, left_y = textbox_border.topleft
        textbox = pygame.Rect(0, 0, width - border * 2, height - border * 2)
        textbox.topleft = (left_x + border, left_y + border)
        return textbox, textbox_border
