import pygame as pg
import pyperclip
from .styles import STYLE
from .abstract_scene import AbstractScene


class PromptInput:
    def __init__(self,
                 screen: pg.Surface,
                 prompt: str,
                 dimension: tuple[int, int] = (768, 64),
                 top_y: int = 65,   # default be at the upper half of the screen
                 top_x: int = 640,  # default be at the middle
                 border: int = 3,
                 font_style: str = "question"):
        # UI components
        # self.scene = scene
        self.screen = screen
        self.prompt = prompt
        self.dimension = dimension
        self.top_y = top_y
        self.top_x = top_x
        self.border = border
        self.font_style = font_style
        # self.prompt_pair, self.inputbox, self.inputbox_border = scene.get_utils(
        # ).create_prompt_with_inputbox(prompt, dimension, top_y, border, font_style)

        # Create the Rects
        self.__create_prompt()

        # state variables
        self.active = False
        self.content = ""

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.active = self.inputbox.collidepoint(event.pos)

        if self.active:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    print(self.prompt, self.content)
                    self.active = False
                elif event.key == pg.K_v and (event.mod & pg.KMOD_CTRL or event.mod & pg.KMOD_META):
                    self.content = pyperclip.paste()
                elif event.key == pg.K_BACKSPACE:
                    self.content = self.content[:-1]
                else:
                    self.content += event.unicode

    def draw(self):
        # screen = self.scene.get_screen()
        screen = self.screen
        screen.blit(*self.prompt_pair)

        color = pg.Color("#8489FBFF") if self.active else pg.Color(
            "#00FF00") if self.content else "black"
        pg.draw.rect(screen, color, self.inputbox_border)
        pg.draw.rect(screen, "white", self.inputbox)

        padding_x, padding_y = 10, 12
        text_surface = STYLE["font"]["text"].render(
            self.content, True, (0, 0, 0))
        # TODO(nickbar01234) - Handle clip text
        screen.blit(text_surface, (self.inputbox.x + padding_x,
                                   self.inputbox.y + self.inputbox.height // 2 - padding_y))

    def get_content(self):
        return self.content

    def __create_prompt(self):
        # screen = self.scene.get_screen()
        screen = self.screen

        # Create the prompt text
        font = STYLE["font"][self.font_style]
        text = font.render(self.prompt, True, "black")
        prompt_rect = text.get_rect()
        prompt_rect.midtop = (self.top_x, self.top_y)

        # Input box rectangle
        input_box_border = pg.Rect(0, 0, *self.dimension)
        input_box_border.midtop = (self.top_x, prompt_rect.bottom + 20)

        input_box = pg.Rect(input_box_border.left + self.border, input_box_border.top + self.border,
                            input_box_border.width - self.border * 2, input_box_border.height - self.border * 2)

        self.prompt_pair = (text, prompt_rect)
        self.inputbox = input_box
        self.inputbox_border = input_box_border
