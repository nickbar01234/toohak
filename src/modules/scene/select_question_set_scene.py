import pygame as pg
from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE
from ..state.question_set import NUM_QUESTIONS, QUESTION_NAMES

import logging
logger = logging.getLogger()


class SelectQuestionSetScene(AbstractScene):
    def __init__(self, screen: pg.Surface, player_state, network):
        super().__init__(screen, player_state, network)

        self.boxes = []
        self.choice: int = -1
        self.question_names = QUESTION_NAMES
        self.question_names.append("Define my own question set")

    def start_scene(self):

        self.__create_options_boxes()
        self.__create_submit_box()

        while True:
            for event in pg.event.get():
                self.handle_quit(event)

                match event.type:
                    case pg.MOUSEBUTTONDOWN:
                        for i, box in enumerate(self.boxes):
                            if box.collidepoint(event.pos):
                                self.choice = i
                                print("Chose idx: %d", i)

                        if self.submit_box.collidepoint(event.pos):
                            print("Confirm choices: %s",
                                  self.question_names[self.choice])
                            self.get_network().choose_default_or_customized(self.choice)
                            if self.choice < len(self.question_names) - 1:
                                return SceneState.REFEREE_START_SCENE
                            else:
                                return SceneState.REFEREE_ADD_QUESTION

            self.get_screen().fill('white')
            self.__draw_submit_box()
            self.__draw_options_boxes()
            pg.display.flip()

    def __create_options_boxes(self):
        width = 400
        height = 100
        x = STYLE['width'] // 2 - width // 2
        y = STYLE['height'] // 5 - height // 2
        spacing = 150

        for i in range(NUM_QUESTIONS + 1):
            box = pg.Rect(x, y + i * spacing, width, height)
            self.boxes.append(box)

    def __draw_options_boxes(self):
        for i, (name, box) in enumerate(zip(self.question_names, self.boxes)):
            color_scheme = STYLE["box_colors"][i % len(STYLE["box_colors"])]
            pg.draw.rect(self.get_screen(
            ), color_scheme["active"] if (i == self.choice) else color_scheme["default"], box)
            text_surface = STYLE["font"]["answer"].render(
                name, True, (0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.center = box.center
            self.get_screen().blit(text_surface, text_rect)

    def __create_submit_box(self):
        self.submit_box, self.submit_box_text, self.submit_text_surface = self.get_utils().create_submit_box(
            "Confirm Question Set")

    def __draw_submit_box(self):
        self.get_utils().draw_submit_box(
            self.submit_box, self.submit_box_text, self.submit_text_surface, color='#af63fb')
