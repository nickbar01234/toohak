import sys
import pygame
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
        # TODO: Who is responsible to render the next question
        idx = 0
        questions = self.get_player_state().get_questions()

        while True:
            if len(questions) == idx:
                return SceneState.QUIT

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            self.get_screen().fill("white")
            questions[idx].draw(self.get_screen())
            pygame.display.flip()
            # idx += 1
