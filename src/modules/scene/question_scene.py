import sys
import pygame as pg
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

    def start_scene(self):
        # TODO: ensure the player selects at least one option
        # TODO: add a box that encloses the option boxes
        option_boxes, optons_box_borders = self.__create_option_boxes()

        submit_box = self.__create_submit_box()

        while True:
            for event in pg.event.get():
                match event.type:
                    case pg.QUIT:
                        pg.quit()
                        sys.exit(0)

                    case pg.MOUSEBUTTONDOWN:
                        if submit_box.collidepoint(event.pos):
                            # note: a janky way of detecting all questions have been answered (we can definitely change this later)
                            if not self.__submit():
                                return SceneState.QUIT
                            continue

                        # update selection
                        for option, box in zip(self.curr_options, option_boxes):
                            if box.collidepoint(event.pos):
                                if option in self.selected:
                                    print(f"You have deselected \"{option}\"!")
                                    self.selected.remove(option)
                                else:
                                    print(f"You have selected \"{option}\"!")
                                    self.selected.add(option)

                                # TODO: add click visual effect (change to a brighter/dimmer color)

            self.get_screen().fill("white")
            self.curr_question.draw(self.get_screen())

            # draw submit box
            pg.draw.rect(self.get_screen(), "lightblue", submit_box)
            submit_text_surface = STYLE["font"]["text"].render(
                "Submit", True, (0, 0, 0))
            self.get_screen().blit(submit_text_surface, (submit_box.x + 10,
                                                         submit_box.y + submit_box.height // 2 - 12))

            # draw next button top right
            # click next
            # build solution
            # verify correct / wrong

            # draw all options
            for i, (option, box) in enumerate(zip(self.curr_options, option_boxes)):
                # print(f"Drawing box with center {box.center}")
                # TESTING
                pg.draw.rect(self.get_screen(),
                             STYLE["box_colors"][i % len(STYLE["box_colors"])], box)
                # TODO: center text
                text_surface = STYLE["font"]["text"].render(
                    option, True, (0, 0, 0))
                self.get_screen().blit(text_surface, box.center)

            pg.display.flip()

    # move to the next question
    def __submit(self):
        print("You are submitting!")
        # TODO: verify solution
        # note: not using the solution builder here cuz it's faster this way
        user_solution = MultipleChoiceSolutionBuilder(self.selected).build()
        print(f"Your solution is {self.selected}")
        correctness = self.curr_question.verify(user_solution)
        print(f"Your answer was {correctness}!")
        # update scene states
        self.q_idx += 1
        if self.num_questions == self.q_idx:
            return False

        self.curr_question = self.get_player_state().get_questions()[
            self.q_idx]
        self.curr_options = self.curr_question.get_options()
        self.selected = set()

        return True

    # TODO: define big border for all options
    # TODO: define templates for 1, 2, 3, and 4 options (we can do this as we cap max options?)

    def __create_submit_box(self):
        dist_from_corner = STYLE["width"] // 40
        box_topright = STYLE["width"] - \
            dist_from_corner, dist_from_corner
        width, height = STYLE["width"] // 15, STYLE["height"] // 15
        box = pg.Rect(0, 0, width, height)
        box.topright = box_topright

        return box

    # when there is only one question
    # def __create_option_boxes_1(self, options):

    def __create_option_boxes(self):
        option_boxes, optons_box_borders = [], []

        border = 3
        # single side
        screen_border_width, screen_border_height = STYLE["width"] * .1, STYLE["height"] * .3
        # TODO: rename variable
        options_zone_width = STYLE["width"] - 2 * screen_border_width
        option_box_center = options_zone_width // (len(self.curr_options) + 1)
        # print(STYLE["width"], options_zone_width)
        # print(option_box_center, option_box_center * 2, option_box_center * 3)

        box_width = options_zone_width // len(self.curr_options) // 2
        box_height = STYLE["height"] * .4
        center_y = screen_border_height + box_height // 2
        # TODO: border between boxes
        # print("Screen width is", STYLE["width"])
        # print("Screen height is", STYLE["height"])

        for i, option in enumerate(self.curr_options):
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
