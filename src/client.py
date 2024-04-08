import pygame
from modules import SceneState, EntryScene, QuestionScene, QuitScene, PlayerState, RoleSelectionScene, NameScene, Network, STYLE

if __name__ == "__main__":
    network = Network()
    screen = pygame.display.set_mode((STYLE["width"], STYLE["height"]))
    pygame.display.set_caption("toohak")

    player_state = PlayerState(network)
    scenes = {
        SceneState.ENTRY: EntryScene(screen, player_state, network),
        SceneState.ROLE_SELECTION: RoleSelectionScene(screen, player_state, network),
        SceneState.PLAYER_NAME: NameScene(screen, player_state, network),
        SceneState.PLAYER_QUESTION: QuestionScene(screen, player_state, network),
        SceneState.QUIT: QuitScene(screen, player_state, network)
    }
    scene = SceneState.ENTRY
    # scene = SceneState.PLAYER_QUESTION

class Client:
    def __init__(self):
        self.network = Network()
        self.state = PlayerState(self.network)
    
    def start(self):
        screen = pygame.display.set_mode((STYLE["height"], STYLE["width"]))
        pygame.display.set_caption("toohak")
        scene = SceneState.ENTRY

        while True:
            scene = SCENES[scene].start_scene()

            # TODO: move to where appropriate
            if scene == SceneState.PLAYER_QUESTION:
                questions = self.network.receive_questions() # block until receive questions
                logger.debug("Received questions: " + str(questions))
                self.state.set_questions(questions)

                # after receiving the questions, start a listner's thread to receive the leadersboard

            
    def server_listener(self):
        logger.info(f"Listener thread waiting for updates from server.")
        while True:
            # TODO: determine when to terminate
            leadersboard = self.network.receive_leadersboard()
            self.state.set_leadersboard(leadersboard)



if __name__ == "__main__":
    client = Client()
    client.start()

    
    

    