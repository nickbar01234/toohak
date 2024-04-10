import logging
import threading
import pygame
from modules import SceneState, EntryScene, QuestionScene, NameScene, QuitScene, PlayerState, RoleSelectionScene, Network, STYLE

logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


class Client:
    def __init__(self):
        self.network = Network()
        self.state = PlayerState(self.network)

    def start(self):
        screen = pygame.display.set_mode((STYLE["width"], STYLE["height"]))
        pygame.display.set_caption("toohak")
        scene = SceneState.ENTRY

        SCENES = {
            # TODO: EntryScene can remove network -> get from player's self.state
            SceneState.ENTRY: EntryScene(screen, self.state, self.network),
            SceneState.PLAYER_NAME: NameScene(screen, self.state, self.network),
            SceneState.ROLE_SELECTION: RoleSelectionScene(screen, self.state, self.network),
            SceneState.PLAYER_QUESTION: QuestionScene(screen, self.state, self.network),
            SceneState.QUIT: QuitScene(screen, self.state, self.network)
        }

        while True:
            scene = SCENES[scene].start_scene()

            if (scene == SceneState.PLAYER_QUESTION):
                logger.info("Client starting a listener thread.")
                listener_thread = threading.Thread(
                    target=self.player_listener, daemon=True)
                listener_thread.start()

    def player_listener(self):
        logger.info(
            "Listener thread started - waits for updates from server for leader's board / terminate sig.")

        questions = self.network.receive_questions()
        self.state.set_questions(questions)
        self.network.receive_game_start()
        self.state.set_game_starts()
        logger.info("Received game starts signal from server.")

        while True:
            leadersboard = self.network.receive_leadersboard()
            self.state.set_leadersboard(leadersboard)
            logger.info("Leader's board updated: %s",
                        self.state.get_leadersboard())

            # gameContinue, leadersboard = self.network.receive_leadersboard_or_game_ends()
        # gameContinue, leadersboard = self.network.receive_leadersboard_or_game_ends()
        # while gameContinue:
        #     leadersboard = self.network.receive_leadersboard()
        #     self.state.set_leadersboard(leadersboard)
        #     logger.info(f"Leader's board updated: {self.state.get_leadersboard}")
        #     gameContinue, leadersboard = self.network.receive_leadersboard_or_game_ends()
        # logger.info(f"Received update from server: Game ends")

        # TODO: wait for and receive Final rank before exiting


if __name__ == "__main__":
    client = Client()
    client.start()
