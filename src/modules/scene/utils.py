import pygame as pg
import pyperclip
from .styles import STYLE
from ..type.aliases import *


class Utils:
    def __init__(self, screen: pg.Surface):
        self.screen = screen

    # old - deprecating
    def create_prompt(self,
                      prompt: str,
                      margin: tuple[int, int],
                      font_style: str = "title"):
        font = STYLE["font"][font_style]
        text = font.render(prompt, True, "black")
        rect = text.get_rect()
        rect.midtop = self.screen.get_rect().midtop
        rect = rect.move(*margin)
        self.screen.blit(text, rect)
        return rect

    # new - create the prompt and input box together
    def create_prompt_with_inputbox(self,
                                    prompt: str = "Add question description",
                                    dimension: tuple[int, int] = (512, 64),
                                    top_y: int = 65,
                                    border: int = 3,
                                    font_style: str = "title"):
        # Create the prompt text
        font = STYLE["font"][font_style]
        text = font.render(prompt, True, "black")
        prompt_rect = text.get_rect()
        prompt_rect.midtop = (self.screen.get_width() // 2, top_y)

        # Input box dimensions
        INPUT_BOX_X = self.screen.get_width() // 2 - dimension[0] // 2

        # Input box rectangle
        input_box_border = pg.Rect(
            (INPUT_BOX_X, prompt_rect.bottom + 20), dimension)
        input_box = pg.Rect(input_box_border.left + border, input_box_border.top + border,
                            input_box_border.width - border * 2, input_box_border.height - border * 2)
        return (text, prompt_rect), input_box, input_box_border

    def draw_prompt_with_inputbox(self, active, filled):
        self.screen.blit(*self.prompt)

        pg.draw.rect(self.get_screen(),
                     pg.Color("#00FF00") if filled
                     else pg.Color("#8489FBFF") if active
                     else "black", self.question_box_border)
        pg.draw.rect(self.get_screen(), "white", self.question_box)

    def create_textbox(self, dimension: tuple[int, int] = (512, 64), border: int = 3):
        textbox_border = pg.Rect(0, 0, *dimension)
        textbox_border.center = self.screen.get_rect().center
        left_x, left_y = textbox_border.topleft
        textbox = pg.Rect(
            0, 0, dimension[0] - border * 2, dimension[1] - border * 2)
        textbox.topleft = (left_x + border, left_y + border)
        return textbox, textbox_border

    def create_button(self, margin: tuple[int, int]):
        border = 3
        width, height = 512, 64
        center_x, center_y = self.screen.get_rect().center
        textbox_border = pg.Rect(0, 0, width, height)
        textbox_border.center = (center_x, center_y)
        textbox_border = textbox_border.move(*margin)
        left_x, left_y = textbox_border.topleft
        textbox = pg.Rect(0, 0, width - border * 2, height - border * 2)
        textbox.topleft = (left_x + border, left_y + border)
        return textbox, textbox_border

    def draw_leadersboard(self, leadersboard: LeadersBoard, ref_rect: pg.Rect):
        for idx, (name, n_questions) in enumerate(leadersboard):
            text = STYLE["font"]["text"].render(
                f"{name}: {n_questions}", True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.midtop = ref_rect.midbottom
            text_rect.top = ref_rect.bottom
            text_rect = text_rect.move(0, ref_rect.height + idx * 32)
            self.screen.blit(text, text_rect)

    def create_submit_box(self, text: str = "Submit"):
        dist_from_corner = STYLE["width"] // 40
        box_topright = STYLE["width"] - \
            dist_from_corner, dist_from_corner
        width, height = STYLE["width"] // 6, STYLE["height"] // 13
        box = pg.Rect(0, 0, width, height)
        box.topright = box_topright

        font = STYLE["font"]["text"]
        submit_text_surface = font.render(text, True, (0, 0, 0))
        text_rect = submit_text_surface.get_rect(center=box.center)
        return box, text_rect, submit_text_surface

    def draw_submit_box(self,
                        submit_box: pg.Rect,
                        text_rect: pg.Rect,
                        text_surface: pg.surface.Surface,
                        color: str = "lightblue"):
        pg.draw.rect(self.screen, color, submit_box)
        self.screen.blit(text_surface, text_rect)

    def create_bottom_right_box(self, text: str):
        dist_from_corner = STYLE["width"] // 40
        box_bottomright = STYLE["width"] - \
            dist_from_corner, STYLE["height"] - dist_from_corner
        width, height = STYLE["width"] // 7, STYLE["height"] // 15
        box = pg.Rect(0, 0, width, height)
        box.bottomright = box_bottomright

        font = STYLE["font"]["text"]
        add_text_surface = font.render(text, True, (0, 0, 0))
        text_rect = add_text_surface.get_rect(center=box.center)
        return box, text_rect, add_text_surface

    def draw_bottom_right_box(self,
                              box: pg.Rect,
                              text_rect: pg.Rect,
                              text_surface: pg.surface.Surface,
                              color: str = "lightblue"):
        pg.draw.rect(self.screen, color, box)
        self.screen.blit(text_surface, text_rect)

    def draw_leaderboard(self, ref_rect: pg.Rect, nquestions: int, leaderboard: list[tuple[str, list[bool], float | None]], display_correctness=False):
        '''
        :param rect Relative anchor point
        :param nquestions Total number of questions
        '''

        left_anchor, top_anchor = ref_rect.topleft
        left_anchor += 128
        box_width = box_height = 48
        box_margin_x = 6
        box_margin_y = 3
        box_radius = 2

        for row, (name, progress, elapsed) in enumerate(leaderboard):
            padded_progress = [None if i >= len(
                progress) else progress[i] for i in range(nquestions)]

            text_name = STYLE["font"]["text"].render(name, True, "black")
            text_name_rect = text_name.get_rect()
            text_name_rect.top = top_anchor + row * \
                (box_height + box_margin_x) + box_height // 2 - 6
            text_name_rect.left = ref_rect.left
            self.screen.blit(text_name, text_name_rect)

            for col, correct in enumerate(padded_progress):
                box_left = left_anchor + col * (box_width + box_margin_y)
                box_top = top_anchor + row * (box_height + box_margin_x)
                box_border = pg.Rect(box_left, box_top, box_width, box_height)
                box = pg.Rect(box_border.left + box_radius, box_border.top + box_radius,
                              box_width - box_radius * 2, box_height - box_radius * 2)

                pg.draw.rect(self.screen, "black", box_border, box_radius, 2)
                if display_correctness:
                    if correct is not None:
                        pg.draw.rect(
                            self.screen, pg.Color("#00FF00") if correct else pg.Color("#FF1B2d"), box)
                    else:
                        # Padded
                        pg.draw.rect(self.screen, "white", box)
                else:
                    pg.draw.rect(self.screen, pg.Color("#d3d3d3") if col <
                                 len(progress) else "white", box)

                if elapsed is not None:
                    elapsed_left = left_anchor + \
                        nquestions * (box_width + box_margin_y)
                    elapsed_top = top_anchor + row * \
                        (box_height + box_margin_x) + box_height // 2 - 8
                    elapsed_text = STYLE["font"]["text"].render(
                        f"{round(elapsed, 2)}s", False, "black")
                    elapsed_rect = elapsed_text.get_rect()
                    elapsed_rect.topleft = (elapsed_left, elapsed_top)
                    self.screen.blit(elapsed_text, elapsed_rect)
