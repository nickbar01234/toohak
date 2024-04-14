import pygame
import threading
from modules.network.network import Network
from modules.state.player_state import PlayerState
from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE
from . import utils


class RoleSelectionScene(AbstractScene):
    def __init__(self, screen: pygame.Surface, player_state: PlayerState, network: Network, role_selection_barrier: threading.Semaphore):
        super().__init__(screen, player_state, network)
        self.__role_selection_barrier = role_selection_barrier

    def start_scene(self):
        referee_box = utils.create_button(self.get_screen(), (0, 0))
        player_box = utils.create_button(self.get_screen(), (0, 100))

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
                    self.get_network().send_mode("referee")
                    self.get_player_state().set_is_player(False)
                    self.__role_selection_barrier.release()
                    return SceneState.REFEREE_START_SCENE

                if event.type == pygame.MOUSEBUTTONDOWN and player_box[0].collidepoint(event.pos):
                    self.get_network().send_mode("player")
                    self.get_player_state().set_is_player(True)
                    self.__role_selection_barrier.release()
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
