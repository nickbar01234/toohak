import sys
import pygame as pg
from time import sleep
from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE
from ..question.multiple_choice_question_builder import MultipleChoiceQuestionBuilder
from ..solution.multiple_choice_solution_builder import MultipleChoiceSolutionBuilder


class QuestionScene(AbstractScene):
    def __init__(self, screen, player_state, network):
        super().__init__(screen, player_state, network)
        # TODO: refactor this later
        player_state.set_questions([
            MultipleChoiceQuestionBuilder()
            .add_question("What's Tony's last name")
            .add_option("Doan")
            .add_option("Xu")
            .add_option("Huang")
            .add_solution(MultipleChoiceSolutionBuilder().add_solution("Huang").build())
            .build(),
            MultipleChoiceQuestionBuilder()
            .add_question("What day is it")
            .add_option("Mon")
            .add_option("Tue")
            .add_option("Wed")
            .add_solution(MultipleChoiceSolutionBuilder().add_solution("Mon").build())
            .build()
        ])

        self.__player_state = player_state
        # TODO: underscore before variable names?
        # TODO: is it good practice to have so many fields?
        self.q_idx = 0
        self.num_questions = len(self.get_player_state().get_questions())
        self.curr_question = self.get_player_state().get_questions()[0]
        self.curr_options = self.curr_question.get_options()
        self.selected = set()
        self.boxes, self.box_borders = self.__create_options_boxes()
        self.submit_box = self.__create_submit_box()

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

                                # TODO: add click visual effect (change to a brighter/dimmer color)

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
        # draw options zone box
        zone_box = self.__create_zone_box()
        pg.draw.rect(self.get_screen(),
                     STYLE["box_colors"][4], zone_box)

        for i, (option, box) in enumerate(zip(self.curr_options, self.boxes)):
            # TESTING
            # print(f"Drawing box with center {box.center}")
            pg.draw.rect(self.get_screen(),
                         STYLE["box_colors"][i % len(STYLE["box_colors"])], box)
            # TODO: center text
            text_surface = STYLE["font"]["text"].render(
                option, True, (0, 0, 0))
            self.get_screen().blit(text_surface, box.center)

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

    def __create_zone_box(self):
        zone_h_space, zone_v_space = STYLE["width"] * .1, STYLE["height"] * .3
        zone_width = STYLE["width"] - 2 * zone_h_space
        zone_height = STYLE["height"] * .4
        center_x = zone_h_space + zone_width // 2
        center_y = zone_v_space + zone_height // 2
        box = pg.Rect(0, 0, zone_width + 10, zone_height + 10)
        box.center = (center_x, center_y)

        return box

    def __create_options_boxes(self):
        boxes, box_borders = [], []

        # spacing between edge of screen and border of options zone that holds all options
        zone_h_space, zone_v_space = STYLE["width"] * .1, STYLE["height"] * .3
        zone_width = STYLE["width"] - 2 * zone_h_space
        center_xs = []

        # different templates for different number of options
        # different width, height and centers
        match len(self.curr_options):
            case 1 | 2 | 3:
                box_center = zone_width // (
                    len(self.curr_options) + 1)
                box_width = zone_width // len(self.curr_options) // 2
                print("Box width is", box_width)
                box_height = STYLE["height"] * .4
                center_y = zone_v_space + box_height // 2

            # grid
            case 4:
                pass

            case _:
                print(
                    f"Cannot have more than 4 options, but somehow we have {len(self.curr_options)} options!")

        # TODO: border between boxes
        # print("Screen width is", STYLE["width"])
        # print("Screen height is", STYLE["height"])

        for i, option in enumerate(self.curr_options):
            # screen_width = left_blank + box + blank + box + blank + box + right_blank
            center_x = zone_h_space + (i + 1) * box_center
            box = pg.Rect(0, 0, box_width, box_height)
            box.center = (center_x, center_y)
            # print(f"Center of option {i} is {center_x, center_y}")
            boxes.append(box)

        return boxes, box_borders
