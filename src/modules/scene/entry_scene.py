import pygame
import pyperclip
from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE


class EntryScene(AbstractScene):
    def start_scene(self):
        print("Inside entry scene")
        clock = pygame.time.Clock()

        ip = ""

        active = False

        while True:
            textbox, textbox_border = self.get_utils().create_textbox()

            for event in pygame.event.get():
                self.handle_quit(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    active = textbox.collidepoint(event.pos)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.get_network().connect(ip)
                        return SceneState.ROLE_SELECTION
                    elif event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL or event.mod & pygame.KMOD_META):
                        ip = pyperclip.paste()
                    elif event.key == pygame.K_BACKSPACE:
                        ip = ip[:-1]
                    else:
                        ip += event.unicode

            self.get_screen().fill("white")

            self.get_utils().create_prompt("Enter server IP address:", (0, 128))

            pygame.draw.rect(self.get_screen(), pygame.Color(
                "#8489FBFF") if active else "black", textbox_border)
            pygame.draw.rect(self.get_screen(), "white", textbox)

            padding_x, padding_y = 10, 12
            text_surface = STYLE["font"]["text"].render(ip, True, (0, 0, 0))
            # TODO(nickbar01234) - Handle clip text
            self.get_screen().blit(text_surface, (textbox.x + padding_x,
                                                  textbox.y + textbox.height // 2 - padding_y))
            pygame.display.flip()

            clock.tick(STYLE["fps"])
