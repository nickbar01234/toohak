from .abstract_scene import AbstractScene
from .scene_state import SceneState


class EntryScene(AbstractScene):
    def start_scene(self):
        # TODO: Implement entry scene
        return SceneState.PLAYER_QUESTION
