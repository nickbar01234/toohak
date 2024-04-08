import sys
import pygame as pg
from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE
from ..question.multiple_choice_question_builder import MultipleChoiceQuestionBuilder
from ..solution.multiple_choice_solution_builder import MultipleChoiceSolutionBuilder


class QuestionScene(AbstractScene):
    def __init__(self, screen, player_state, network):
        super().__init__(screen, player_state, network)
        player_state.set_questions([
            MultipleChoiceQuestionBuilder()
            .add_question("What's Tony's last name")
            .add_option("Doan")
            .add_option("Xu")
            .add_option("Huang")
            .add_solution(MultipleChoiceSolutionBuilder().add_solution("Huang").build())
            .build()
        ])
        self.__player_state = player_state

    def start_scene(self):
        # TODO: Who is responsible to render the next question
        q_idx = 0
        questions = self.get_player_state().get_questions()
        # TODO: change questions
        options = questions[q_idx].get_options()
        option_boxes, optons_box_borders = self.__create_option_boxes(options)
        # TODO: add a box that encloses the option boxes
        box_colors = ["red", "green", "blue", "yellow", "purple"]
        print(options)

        while True:
            if len(questions) == q_idx:
                return SceneState.QUIT

            for event in pg.event.get():
                match event.type:
                    case pg.QUIT:
                        pg.quit()
                        sys.exit(0)

                    case pg.MOUSEBUTTONDOWN:
                        active = [box.collidepoint(event.pos)
                                  for box in option_boxes]
                        for option, clicked in zip(options, active):
                            if clicked:
                                print(f"You have selected \"{option}\"!")
                                # TODO: add click visual effect (change to a brighter/dimmer color)
                                # TODO: verify solution
                                # TODO: update player state and current scene state vars
                                # q_idx += 1
                                # update options
                                # TODO: maybe add a next_question method?
                                options = questions[q_idx].get_options()

            self.get_screen().fill("white")
            questions[q_idx].draw(self.get_screen())

            for i, (option, box) in enumerate(zip(options, option_boxes)):
                # print(f"Drawing box with center {box.center}")
                # TESTING
                pg.draw.rect(self.get_screen(),
                             box_colors[i % len(box_colors)], box)
                # TODO: center text
                text_surface = STYLE["font"]["text"].render(
                    option, True, (0, 0, 0))
                self.get_screen().blit(text_surface, box.center)

            pg.display.flip()

    def __create_option_boxes(self, options):
        option_boxes, optons_box_borders = [], []

        border = 3
        # single side
        screen_border_width, screen_border_height = STYLE["width"] * .1, STYLE["height"] * .3
        # TODO: rename variable
        options_zone_width = STYLE["width"] - 2 * screen_border_width
        option_box_center = options_zone_width // (len(options) + 1)
        # print(STYLE["width"], options_zone_width)
        # print(option_box_center, option_box_center * 2, option_box_center * 3)

        box_width = options_zone_width // len(options) // 2
        box_height = STYLE["height"] * .4
        center_y = screen_border_height + box_height // 2
        # TODO: border between boxes
        # print("Screen width is", STYLE["width"])
        # print("Screen height is", STYLE["height"])

        for i, option in enumerate(options):
            # screen_width =
            # left_blank + box + blank + box + blank + box + right_blank
            center_x = screen_border_width + (i + 1) * option_box_center
            option_box = pg.Rect(0, 0, box_width, box_height)
            option_box.center = (center_x, center_y)
            # print(f"Center of option {i} is {center_x, center_y}")
            option_boxes.append(option_box)

        # width, height = 512, 64
        # center_x, center_y = self.get_screen().get_rect().center
        # textbox_border = pg.Rect(0, 0, width, height)
        # textbox_border.center = (center_x, center_y)
        # left_x, left_y = textbox_border.topleft
        # textbox = pg.Rect(0, 0, width - border * 2, height - border * 2)
        # textbox.topleft = (left_x + border, left_y + border)

        return option_boxes, optons_box_borders
