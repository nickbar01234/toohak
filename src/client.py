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

    while True:
        scene = scenes[scene].start_scene()
