import sys
import threading
import pygame as pg
from .abstract_scene import AbstractScene
from .scene_state import SceneState
from .styles import STYLE
from .prompt_input_box import PromptInput
from ..type.aliases import *
from ..question.multiple_choice_question_builder import MultipleChoiceQuestionBuilder
from ..solution.multiple_choice_solution_builder import MultipleChoiceSolutionBuilder
# from ..state.player_state import PlayerState
# from ..network import Network


class AddQuestionScene(AbstractScene):

    def __init__(self, screen: pg.Surface, player_state, network):
        super().__init__(screen, player_state, network)

        self.questions: list[Question] = []
        self.question_description = ""
        self.__create_submit_box()
        self.__create_add_box()

        self.__question_prompt = PromptInput(
            self.get_screen(), "Add question description: ")
        self.__option_prompts: list[PromptInput] = [
            PromptInput(self.get_screen(), "Option A: ", top_y=250)
        ]

        self.senders: list[threading.Thread] = []
        # TODO: create a variable / way to store and prompt the solution!

    def start_scene(self):
        # TODO(nickbar01234) - Need to extract into a input class
        clock = pg.time.Clock()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)

                self.__question_prompt.handle_event(event)
                _ = [p.handle_event(event) for p in self.__option_prompts]

                if event.type == pg.MOUSEBUTTONDOWN:
                    # Finish and submit:
                    if self.submit_box.collidepoint(event.pos):
                        self.__collect_and_send_current_question()

                        # wait for all senders to be done
                        for sender in self.senders:
                            sender.join()

                        # TODO: return the next SceneState here!!

                    elif self.add_box.collidepoint(event.pos):
                        self.__collect_and_send_current_question()

                        # TODO: clear the current input and state & redraw!!!

            self.get_screen().fill("white")
            self.__draw_buttons()

            self.__question_prompt.draw()
            _ = [p.draw() for p in self.__option_prompts]
            # TODO: draw more

            pg.display.flip()
            clock.tick(STYLE["fps"])

    #
    # Protocols for state management & sending messages
    #
    def __collect_and_send_current_question(self):
        question = self.__build_and_add_question()

        sender = threading.Thread(target=self.sender, args=question)
        self.senders.append(sender)
        sender.start()

    def __build_and_add_question(self):
        # Collect the current question, options and solution
        builder = MultipleChoiceQuestionBuilder() .add_question(
            self.__question_prompt.get_content())

        for option_prompt in self.__option_prompts:
            builder = builder.add_option(
                option_prompt.get_content())

        builder = builder.add_solution(
            MultipleChoiceSolutionBuilder().add_solution("TODO - THIS IS A PLACE HOLDER"))
        # TODO: implement a user-friendly way to select the solution!!

        question = builder.build()

        # Add to the question bank TODO: necessary?????????????
        self.questions.append(question)

        return question

    def __sender(question: Question):
        pass  # TODO: IMPLEMENT SENDER

    #
    # UI drawing & rendering
    #

    def __create_submit_box(self):
        self.submit_box, self.submit_box_text, self.submit_text_surface = self.get_utils().create_submit_box(
            "Finish and Submit")

    def __create_add_box(self):
        self.add_box, self.add_box_text, self.add_text_surface = self.get_utils().create_bottom_right_box(
            "Add")

    def __draw_buttons(self):
        self.get_utils().draw_submit_box(
            self.submit_box, self.submit_box_text, self.submit_text_surface)
        self.get_utils().draw_bottom_right_box(
            self.add_box, self.add_box_text, self.add_text_surface)

    def __submit(self):
        # logger.info("Referee submits questions")
        # TODO: broadcast the start game signal to all players
        print("Referee submits questions")
