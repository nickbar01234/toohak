import sys
import pygame as pg
from time import sleep
from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE
from ..question.multiple_choice_question_builder import MultipleChoiceQuestionBuilder
from ..solution.multiple_choice_solution_builder import MultipleChoiceSolutionBuilder


class QuestionScene(AbstractScene):
    # def __init__(self, screen, player_state, network):
    #     super().__init__(screen, player_state, network)
    #     player_state.set_questions([
    #         MultipleChoiceQuestionBuilder()
    #         .add_question("What's Tony's last name")
    #         .add_option("Doan")
    #         .add_option("Xu")
    #         .add_option("Huang")
    #         .add_solution(MultipleChoiceSolutionBuilder().add_solution("Huang").build())
    #         .build()
    #     ])

    # TODO: add the network choice for updating the player's progress (question scene) to the server after merge

    # TODO: add the network choice for updating the player's progress (question scene) to the server after merge 

    def start_scene(self):
        # TODO: ensure the player selects at least one option
        # TODO: add a box that encloses the option boxes

        while True:
            for event in pg.event.get():
                match event.type:
                    case pg.QUIT:
                        pg.quit()
                        sys.exit(0)

                    case pg.MOUSEBUTTONDOWN:
                        if self.submit_box.collidepoint(event.pos):
                            # note: a janky way of detecting all questions have been answered (we can definitely change this later)
                            if not self.__submit():
                                return SceneState.QUIT
                            continue

                        # update selection
                        for option, box in zip(self.curr_options, self.boxes):
                            if box.collidepoint(event.pos):
                                if option in self.selected:
                                    print(f"You have deselected \"{option}\"!")
                                    self.selected.remove(option)
                                else:
                                    print(f"You have selected \"{option}\"!")
                                    self.selected.add(option)

            self.get_screen().fill("white")
            self.curr_question.draw(self.get_screen())

            # draw submit box
            pg.draw.rect(self.get_screen(), "lightblue", self.submit_box)
            submit_text_surface = STYLE["font"]["text"].render(
                "Submit", True, (0, 0, 0))
            self.get_screen().blit(submit_text_surface, (self.submit_box.x + 10,
                                                         self.submit_box.y + self.submit_box.height // 2 - 12))

            # draw all options
            self.__draw_options()

            pg.display.flip()

    # move to the next question
    def __submit(self):
        print("You are submitting!")
        user_solution = MultipleChoiceSolutionBuilder(self.selected).build()
        print(f"Your solution is {self.selected}")
        correctness = self.curr_question.verify(user_solution)
        self.__draw_correctness(correctness)

        # update scene states
        self.q_idx += 1
        if self.num_questions == self.q_idx:
            return False

        self.curr_question = self.get_player_state().get_questions()[
            self.q_idx]
        self.curr_options = self.curr_question.get_options()
        self.selected = set()
        self.boxes, self.box_borders = self.__create_options_boxes()
        self.__player_state.set_progress(correctness)
        # TODO: send udpated progress to server

        return True

    def __draw_correctness(self, correctness):
        text = STYLE["font"]["title"].render(
            f"Your answer was {correctness}!", True, (0, 0, 0))
        rect = text.get_rect()
        rect.center = self.get_screen().get_rect().center
        self.get_screen().fill("white")
        self.get_screen().blit(text, rect)
        pg.display.flip()
        sleep(1)

    def __draw_options(self):
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

    def __create_submit_box(self):
        dist_from_corner = STYLE["width"] // 40
        box_topright = STYLE["width"] - \
            dist_from_corner, dist_from_corner
        width, height = STYLE["width"] // 15, STYLE["height"] // 15
        box = pg.Rect(0, 0, width, height)
        box.topright = box_topright

        return box

    def __create_options_boxes(self):
        boxes, box_borders = [], []

        # spacing between edge of screen and border of options zone that holds all options
        container = pg.Rect(0, 0, STYLE["width"] * 0.9, STYLE["height"] * 0.6)
        container.center = self.get_screen().get_rect().center
        container.bottom = self.get_screen().get_rect().bottom

        margin_x, margin_y = 16, 32
        width, height = container.width // 2, 100
        row = 0
        for idx in range(len(self.curr_options)):
            box = pg.Rect(container.left + (idx % 2) * width + margin_x,
                          container.top + (row * (height + margin_y)), width - margin_x * 2, height)
            boxes.append(box)
            if idx % 2 != 0:
                row += 1

        return boxes, box_borders
