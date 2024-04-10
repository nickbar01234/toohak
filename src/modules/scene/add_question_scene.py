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
        # self.add_question_box = self.__create_add_question_box()

    def start_scene(self):
        while True:
            for event in pg.event.get():
                self.handle_quit(event)
                match event.type:
                    case pg.MOUSEBUTTONDOWN:
                        # submit
                        if self.submit_box.collidepoint(event.pos):
                            self.__submit()
                            return SceneState.REFEREE_MONITOR

                        # add question
                        # if self.add_question_box.collidepoint(event.pos):
                        #     self.__add_question(question)

            self.get_screen().fill("white")
            utils.draw_submit_box(
                self.get_screen(), "lightblue", self.submit_box)
            pg.display.flip()

    def __add_question(self, question):
        self.questions.append(question)

    def __create_add_question_box(self):
        pass

    def __submit(self):
        # logger.info("Referee submits questions")
        # TODO: broadcast the start game signal to all players
        print("Referee submits questions")
