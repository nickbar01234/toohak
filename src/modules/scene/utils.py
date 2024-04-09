import pygame as pg
from .styles import STYLE


def create_prompt(screen: pg.Surface, prompt: str, margin: tuple[int, int]):
    font = STYLE["font"]["title"]
    text = font.render(prompt, True, "black")
    rect = text.get_rect()
    rect.midtop = screen.get_rect().midtop
    rect = rect.move(*margin)
    screen.blit(text, rect)


def create_textbox(screen: pg.Surface, dimension: tuple[int, int] = (512, 64), border: int = 3):
    textbox_border = pg.Rect(0, 0, *dimension)
    textbox_border.center = screen.get_rect().center
    left_x, left_y = textbox_border.topleft
    textbox = pg.Rect(
        0, 0, dimension[0] - border * 2, dimension[1] - border * 2)
    textbox.topleft = (left_x + border, left_y + border)
    return textbox, textbox_border
