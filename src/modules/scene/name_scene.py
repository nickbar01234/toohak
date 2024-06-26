import sys
import pygame
import pyperclip
from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE


class NameScene(AbstractScene):
    def start_scene(self):
        # TODO(nickbar01234) - Need to extract into a input class
        clock = pygame.time.Clock()
        name = ""
        failed_name = ""
        active = False
        while True:
            textbox, textbox_border = self.get_utils().create_textbox()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    active = textbox.collidepoint(event.pos)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.get_network().send_name(name):
                            self.get_player_state().player_start_barrier.release()
                            return SceneState.PLAYER_WAIT_START_ROOM
                        else:
                            failed_name = name
                    elif event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL or event.mod & pygame.KMOD_META):
                        name = pyperclip.paste()
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

            self.get_screen().fill("white")

            self.get_utils().create_prompt("Enter your name:", (0, 128))

            pygame.draw.rect(self.get_screen(), pygame.Color(
                "#8489FBFF") if active else "black", textbox_border)
            pygame.draw.rect(self.get_screen(), "white", textbox)

            padding_x, padding_y = 10, 12
            text_surface = STYLE["font"]["text"].render(name, True, (0, 0, 0))
            # TODO(nickbar01234) - Handle clip text
            self.get_screen().blit(text_surface, (textbox.x + padding_x,
                                                  textbox.y + textbox.height // 2 - padding_y))

            if failed_name == name and len(name) > 0:
                error_msg = STYLE["font"]["text"].render(
                    f"'{failed_name}' has been taken on the server", True, "red")
                error_msg_rect = error_msg.get_rect()
                error_msg_rect.top = textbox_border.bottom + 16
                error_msg_rect.left = textbox_border.left
                self.get_screen().blit(error_msg, error_msg_rect)

            pygame.display.flip()

            clock.tick(STYLE["fps"])
