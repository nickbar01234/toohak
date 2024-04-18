import logging
import threading
import pygame as pg
from modules import SceneState, EntryScene, AddQuestionScene,  QuestionScene, NameScene, WaitScene, QuitScene, PlayerState, RoleSelectionScene, RefreeStartScene, AddQuestionScene, MonitorScene, Network, STYLE

logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


class Client:
    def __init__(self):
        self.network = Network()
        self.state = PlayerState(self.network)

    def start(self):
        screen = pg.display.set_mode((STYLE["width"], STYLE["height"]))
        pg.display.set_caption("toohak")
        scene = SceneState.ENTRY

        SCENES = {
            # TODO: EntryScene can remove network -> get from player's self.state
            # SceneState.ENTRY: AddQuestionScene(screen, self.state, self.network),
            SceneState.ENTRY: EntryScene(screen, self.state, self.network),
            SceneState.ROLE_SELECTION: RoleSelectionScene(screen, self.state, self.network),

            # Player scenes
            SceneState.PLAYER_NAME: NameScene(screen, self.state, self.network),
            SceneState.PLAYER_WAIT_START_ROOM: WaitScene(screen, self.state, self.network, "You're in! We're waiting for other players to get ready...", SceneState.PLAYER_QUESTION, self.state.game_starts),
            SceneState.PLAYER_QUESTION: QuestionScene(screen, self.state, self.network),
            SceneState.PLAYER_WAIT_END_ROOM: WaitScene(
                screen, self.state, self.network, "We're waiting for the server to compute the results...", SceneState.QUIT, self.state.game_end_barrier),
            SceneState.QUIT: QuitScene(screen, self.state, self.network),

            # Referee scenes
            SceneState.REFEREE_START_SCENE: RefreeStartScene(screen, self.state, self.network),
            SceneState.REFEREE_ADD_QUESTION: AddQuestionScene(screen, self.state, self.network),
            SceneState.REFEREE_MONITOR: MonitorScene(screen, self.state, self.network),
        }

        music_thread = threading.Thread(target=self.music_thread, daemon=True)
        music_thread.start()

        listener_thread = threading.Thread(
            target=self.listener, daemon=True)
        listener_thread.start()

        try:
            while True:
                logger.info("On scene %s", scene)
                scene = SCENES[scene].start_scene()
        except KeyboardInterrupt:
            self.network.disconnect()

    def listener(self):
        logger.info("Runing listener")

        # expect to release in role scene
        self.state.role_selection_barrier.acquire()
        role = "player" if self.state.get_is_player() else "referee"
        logger.info(f"Finished selecting role, selected {role}")

        if self.state.get_is_player():
            self.player_role()
        else:
            self.referee_role()

    def player_role(self):
        try:
            # expect to release in name scene
            self.state.player_start_barrier.acquire()

            logger.info("Waiting for questions")
            questions = self.network.receive_questions()
            self.state.set_questions(questions)
            logger.info("Received questions.")

            init_leadersboard = self.network.block_until_game_starts()
            self.state.set_leadersboard(init_leadersboard)
            self.state.game_starts.release()

            game_continues, leadersboard = self.network.receive_leadersboard_or_game_ends()
            while game_continues:
                self.state.set_leadersboard(leadersboard)
                logger.info(
                    "Leader's board updated: {%s}", self.state.get_leadersboard())
                game_continues, leadersboard = self.network.receive_leadersboard_or_game_ends()

            self.state.set_leadersboard(leadersboard)
            self.state.game_end_barrier.release()
        except Exception as _:
            self.network.disconnect()

    def referee_role(self):
        logger.info("Waiting for questions")
        init_leadersboard = self.network.receive_leadersboard()
        self.state.set_leadersboard(init_leadersboard)

        game_continues, leadersboard = self.network.receive_leadersboard_or_game_ends()
        while game_continues:
            self.state.set_leadersboard(leadersboard)
            logger.info(
                "Leader's board updated: {%s}", self.state.get_leadersboard())
            game_continues, leadersboard = self.network.receive_leadersboard_or_game_ends()

        self.network.block_until_game_ends()
        logger.info("Received update from server: Game ends")

    def music_thread(self):
        pg.mixer.music.load("assets/music/toohak_song.mp3")
        # pg.mixer.music.play(loops=-1)


if __name__ == "__main__":
    client = Client()
    client.start()
