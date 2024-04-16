import sys
import random
import pygame as pg
import pyperclip
from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE
from . import utils
# from ..state.player_state import PlayerState
# from ..network import Network


class AddQuestionScene(AbstractScene):
    def __init__(self, screen: pg.Surface, player_state, network):
        super().__init__(screen, player_state, network)

        self.questions = []
        self.submit_box = utils.create_submit_box()
        self.add_box = utils.create_add_box()
        # self.add_question_box = self.__create_add_question_box()

    def start_scene(self):
        # TODO(nickbar01234) - Need to extract into a input class
        clock = pg.time.Clock()
        question = ""
        active = False
        while True:
            question_box, question_box_border = utils.create_textbox(
                self.get_screen(), dimension=(768, 64), distance_to_top=70)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)

                if event.type == pg.MOUSEBUTTONDOWN:
                    active = question_box.collidepoint(event.pos)

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.__add_question(question)
                        print(self.questions)
                        # TODO: return the next scene here
                    elif event.key == pg.K_v and (event.mod & pg.KMOD_CTRL or event.mod & pg.KMOD_META):
                        question = pyperclip.paste()
                    elif event.key == pg.K_BACKSPACE:
                        question = question[:-1]
                    else:
                        question += event.unicode

            self.get_screen().fill("white")
            utils.draw_submit_box(
                self.get_screen(), self.submit_box, text="Finish and Submit")
            utils.draw_add_box(self.get_screen(),
                               self.add_box, text="Add Question")

            utils.create_prompt(self.get_screen(),
                                "Add Question:", (0, 20), "question")

            pg.draw.rect(self.get_screen(), pg.Color(
                "#8489FBFF") if active else "black", question_box_border)
            pg.draw.rect(self.get_screen(), "white", question_box)

            padding_x, padding_y = 10, 12
            text_surface = STYLE["font"]["text"].render(
                question, True, (0, 0, 0))
            # TODO(nickbar01234) - Handle clip text
            self.get_screen().blit(text_surface, (question_box.x + padding_x,
                                                  question_box.y + question_box.height // 2 - padding_y))
            pg.display.flip()

            clock.tick(STYLE["fps"])

    def __add_question(self, question):
        self.questions.append(question)
        print("Question added: ", question)

    def __create_add_question_box(self):
        pass

    def __submit(self):
        # logger.info("Referee submits questions")
        # TODO: broadcast the start game signal to all players
        print("Referee submits questions")
