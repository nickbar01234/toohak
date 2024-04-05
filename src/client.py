import pygame
from modules import SceneState, EntryScene, QuestionScene, QuitScene, PlayerState, STYLE

if __name__ == "__main__":
    screen = pygame.display.set_mode((STYLE["height"], STYLE["width"]))
    pygame.display.set_caption("toohak")

    scenes = {
        SceneState.ENTRY: EntryScene(screen, PlayerState(None), None),
        SceneState.PLAYER_QUESTION: QuestionScene(screen, PlayerState(None), None),
        SceneState.QUIT: QuitScene(screen, PlayerState(None), None)
    }
    scene = SceneState.ENTRY

    while True:
        scene = scenes[scene].start_scene()
