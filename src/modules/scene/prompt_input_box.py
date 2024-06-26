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
                 font_style: str = "question",
                 add_check_box: bool = False):
        # UI components
        self.screen = screen
        self.prompt = prompt
        self.dimension = dimension
        self.top_y = top_y
        self.top_x = top_x
        self.border = border
        self.font_style = font_style
        self.add_check_box = add_check_box

        # conditional rects
        self.check_box_triple = None

        # Create the Rects
        self.__create_prompt()

        # state variables
        self.active = False
        self.content = ""
        self.correct_answer = False

    # Only return true if it turns correct_answer = True by the current click!

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.active = self.inputbox.collidepoint(event.pos)
            if self.add_check_box:
                check_box, _ = self.check_box_triple
                if check_box.collidepoint(event.pos):
                    self.correct_answer = not self.correct_answer

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
        font = STYLE["font"]["text"]
        # draw the prompt text
        screen = self.screen
        screen.blit(*self.prompt_pair)

        # draw the checkbox if needed
        if self.add_check_box:
            if self.correct_answer:
                color = "green4"
                border, inner = self.check_box_triple
                pg.draw.rect(screen, color, border)

                text_surface = STYLE["font"]["text"].render(
                    "Correct Answer!", True, color)
                text_rect = text_surface.get_rect()
                text_rect.topleft = border.topright
                screen.blit(text_surface, text_rect)
            else:
                border, inner = self.check_box_triple
                pg.draw.rect(screen, "black", border)
                pg.draw.rect(screen, "white", inner)

                text_surface = STYLE["font"]["text"].render(
                    "Correct Answer?", True, "black")
                text_rect = text_surface.get_rect()
                text_rect.topleft = border.topright
                screen.blit(text_surface, text_rect)

        # draw the input box
        color = pg.Color("#8489FBFF") if self.active else pg.Color(
            "#00FF00") if self.content else "black"
        pg.draw.rect(screen, color, self.inputbox_border)
        pg.draw.rect(screen, "white", self.inputbox)

        padding_x, padding_y = 10, 12
        text_surface = font.render(self.content, True, (0, 0, 0))
        # TODO(nickbar01234) - Handle clip text
        screen.blit(text_surface, (self.inputbox.x + padding_x,
                                   self.inputbox.y + self.inputbox.height // 2 - padding_y))

    def get_content(self):
        return self.content

    def get_correct_answer(self) -> bool:
        return self.correct_answer

    def set_correct_answer(self, is_correct: bool):
        self.correct_answer = is_correct

    def __create_prompt(self):
        # Create the prompt text
        font = STYLE["font"][self.font_style]
        text = font.render(self.prompt, True, "black")
        prompt_rect = text.get_rect()
        prompt_rect.midtop = (self.top_x, self.top_y)

        # Create the check-box if needed
        if self.add_check_box:
            check_box_border = pg.Rect(
                prompt_rect.right + 20, prompt_rect.top, 20, 20)
            border = 3
            check_box_rect = pg.Rect(check_box_border.left + border, check_box_border.top + border,
                                     check_box_border.width - border * 2, check_box_border.width - border * 2)
            self.check_box_triple = (check_box_border, check_box_rect)

        # Input box rectangle
        input_box_border = pg.Rect(0, 0, *self.dimension)
        input_box_border.midtop = (self.top_x, prompt_rect.bottom + 20)

        self.inputbox = pg.Rect(input_box_border.left + self.border, input_box_border.top + self.border,
                                input_box_border.width - self.border * 2, input_box_border.height - self.border * 2)

        self.prompt_pair = (text, prompt_rect)
        self.inputbox_border = input_box_border
