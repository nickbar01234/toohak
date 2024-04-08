import pygame
from modules import SceneState, EntryScene, QuestionScene, QuitScene, PlayerState, RoleSelectionScene, Network, STYLE

if __name__ == "__main__":
    network = Network()
    screen = pygame.display.set_mode((STYLE["height"], STYLE["width"]))
    pygame.display.set_caption("toohak")

    scenes = {
        SceneState.ENTRY: EntryScene(screen, PlayerState(network), network),
        SceneState.ROLE_SELECTION: RoleSelectionScene(screen, PlayerState(network), network),
        SceneState.PLAYER_QUESTION: QuestionScene(screen, PlayerState(network), network),
        SceneState.QUIT: QuitScene(screen, PlayerState(network), network)
    }
    scene = SceneState.ENTRY

    while True:
        scene = scenes[scene].start_scene()
