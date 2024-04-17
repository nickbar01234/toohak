import pygame as pg
import pyperclip
from .styles import STYLE


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
