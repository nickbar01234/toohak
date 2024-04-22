import time
from datetime import datetime
import logging
import pygame as pg
from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE
from ..solution.multiple_choice_solution_builder import MultipleChoiceSolutionBuilder

logger = logging.getLogger()
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


class QuestionScene(AbstractScene):
    def start_scene(self):
        # Now initialize the questions when starting the scene
        self.q_idx = 0
        self.num_questions = len(self.get_player_state().get_questions())
        self.curr_question = self.get_player_state().get_questions()[0]
        self.curr_options = self.curr_question.get_options()
        self.selected = set()
        self.container, self.boxes, self.box_borders = self.__create_options_boxes()
        self.submit_box, self.submit_box_text, self.submit_text_surface = self.get_utils(
        ).create_submit_box()

        # TODO: ensure the player selects at least one option
        # TODO: add a box that encloses the option boxes

        self.get_player_state().set_init_time()

        while True:
            n_selection = len(self.curr_question.get_solution().get_solution())

            for event in pg.event.get():
                self.handle_quit(event)
                match event.type:
                    case pg.MOUSEBUTTONDOWN:
                        # update selection
                        # If one solution, submit.
                        # If multi-selection and enough chosen, submit
                        for option, box in zip(self.curr_options, self.boxes):
                            if box.collidepoint(event.pos):
                                if option in self.selected:
                                    self.selected.remove(option)
                                else:
                                    self.selected.add(option)

                                # TODO(nickbar01234) - Extract into components?
                                if len(self.selected) == n_selection:
                                    user_solution = MultipleChoiceSolutionBuilder(
                                        self.selected).build()
                                    correctness = self.curr_question.verify(
                                        user_solution)

                                    self.get_player_state().set_progress(correctness)
                                    self.get_network().update_progress(self.get_player_state().get_progress())
                                    self.__draw_correctness(correctness)
                                    self.q_idx += 1
                                    if self.num_questions == self.q_idx:
                                        delta = datetime.now() - self.get_player_state().get_init_time()
                                        self.get_network().send_elapsed_time(delta.total_seconds())
                                        return SceneState.PLAYER_WAIT_END_ROOM

                                    self.curr_question = self.get_player_state().get_questions()[
                                        self.q_idx]
                                    self.curr_options = self.curr_question.get_options()
                                    self.selected = set()
                                    self.container, self.boxes, self.box_borders = self.__create_options_boxes()

            self.get_screen().fill("white")

            question_rect = self.get_utils().create_prompt(
                self.curr_question.get_question(), (0, 0), "question")

            question_number_text = STYLE["font"]["text"].render(
                f"Question {self.q_idx + 1} / {len(self.get_player_state().get_questions())}", True, pg.Color("#949494"))
            question_number_text_rect = question_number_text.get_rect()
            question_number_text_rect.topright = self.get_screen().get_rect().topright
            question_number_text_rect = question_number_text_rect.move(-15, 10)
            self.get_screen().blit(question_number_text, question_number_text_rect)

            if n_selection > 1:
                select_text = STYLE["font"]["text"].render(
                    f"(Select {n_selection} options)", True, pg.Color("#949494"))
                select_rect = select_text.get_rect()
                select_rect.midtop = question_rect.midbottom
                self.get_screen().blit(select_text, select_rect)
                question_rect = select_rect

            leaderboard_box = self.get_utils().create_leaderboard_box()
            self.get_utils().draw_leaderboard(leaderboard_box, 20,
                                              self.get_player_state().get_leadersboard())

            # draw all options
            self.__draw_options()
            pg.display.flip()

    def __draw_correctness(self, correctness):
        text = STYLE["font"]["title"].render(
            f"Your answer was {correctness}!", True, (0, 0, 0))
        rect = text.get_rect()
        rect.center = self.get_screen().get_rect().center
        self.get_screen().fill("white")
        self.get_screen().blit(text, rect)
        pg.display.flip()
        time.sleep(1)

    def __draw_options(self):
        pg.draw.rect(self.get_screen(), "black", self.container)

        border = 3
        inner_box = pg.Rect(self.container.left + border, self.container.top + border,
                            self.container.width - border * 2, self.container.height - border * 2)
        pg.draw.rect(self.get_screen(), "white", inner_box)
        for i, (option, box) in enumerate(zip(self.curr_options, self.boxes)):
            selected = option in self.selected
            color_scheme = STYLE["box_colors"][i % len(STYLE["box_colors"])]
            pg.draw.rect(self.get_screen(
            ), color_scheme["active"] if selected else color_scheme["default"], box)
            text_surface = STYLE["font"]["answer"].render(
                option, True, (0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.center = box.center
            self.get_screen().blit(text_surface, text_rect)

    def __create_options_boxes(self):
        boxes, box_borders = [], []

        # spacing between edge of screen and border of options zone that holds all options
        container = pg.Rect(0, 0, STYLE["width"] * 0.9, STYLE["height"] * 0.6)
        container.top = self.get_screen().get_rect().centery
        container.centerx = self.get_screen().get_rect().centerx

        margin_x, margin_y = 16, 32
        width, height = container.width // 2, 100
        row = 0
        for idx in range(len(self.curr_options)):
            box = pg.Rect(container.left + (idx % 2) * width + margin_x,
                          container.top + 80 + (row * (height + margin_y)), width - margin_x * 2, height)
            boxes.append(box)
            if idx % 2 != 0:
                row += 1

        return container, boxes, box_borders
