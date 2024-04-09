import pygame
import logging
import threading
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
            SceneState.ROLE_SELECTION: RoleSelectionScene(screen, self.state, self.network),
            SceneState.PLAYER_QUESTION: QuestionScene(screen, self.state, self.network),
            SceneState.QUIT: QuitScene(screen, self.state, self.network)
        }

        while True:
            scene = SCENES[scene].start_scene()

            # TODO: move to where appropriate
            if scene == SceneState.PLAYER_QUESTION:
                questions = self.network.receive_questions()  # block until receive questions
                logger.debug("Received questions: " + str(questions))
                self.state.set_questions(questions)

                logger.info(f"Waiting for game to be started.")
                self.network.receive_game_start()  # block until game starts
                logger.info(f"Game starts")

                # start a listner's thread to receive updates from the server (the leadersboard and game ends sig)
                listener_thread = threading.Thread(target=self.server_listener)
                listener_thread.start()

    def server_listener(self):
        logger.info(f"Listener thread waiting for game to start from server.")

        # TODO: wait for a message for game starts
        self.network.receive_game_start()  # block until game starts

        logger.info(
            f"Game starts; Listener now waits for updates from server for leader's board / terminate sig.")

        while True:
            leadersboard = self.network.receive_leadersboard()
            self.state.set_leadersboard(leadersboard)
            logger.info(f"Leader's board updated: {
                self.state.get_leadersboard}")
            # gameContinue, leadersboard = self.network.receive_leadersboard_or_game_ends()
            # gameContinue, leadersboard = self.network.receive_leadersboard_or_game_ends()
            # while gameContinue:
            #     leadersboard = self.network.receive_leadersboard()
            #     self.state.set_leadersboard(leadersboard)
            #     logger.info(f"Leader's board updated: {self.state.get_leadersboard}")
            #     gameContinue, leadersboard = self.network.receive_leadersboard_or_game_ends()
            # logger.info(f"Received update from server: Game ends")

            # TODO: wait for and receive Final rank before exiting

            # TODO: wait for and receive Final rank before exiting


if __name__ == "__main__":
    client = Client()
    client.start()
