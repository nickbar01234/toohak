import pygame as pg
from .styles import STYLE


def create_prompt(screen: pg.Surface, prompt: str, margin: tuple[int, int], font_style: str = "title"):
    font = STYLE["font"][font_style]
    text = font.render(prompt, True, "black")
    rect = text.get_rect()
    rect.midtop = screen.get_rect().midtop
    rect = rect.move(*margin)
    screen.blit(text, rect)


# def create_textbox(screen: pg.Surface, dimension: tuple[int, int] = (512, 64), border: int = 3):
#     textbox_border = pg.Rect(0, 0, *dimension)
#     textbox_border.center = screen.get_rect().center
#     left_x, left_y = textbox_border.topleft
#     textbox = pg.Rect(
#         0, 0, dimension[0] - border * 2, dimension[1] - border * 2)
#     textbox.topleft = (left_x + border, left_y + border)
#     return textbox, textbox_border


def create_textbox(screen: pg.Surface, dimension: tuple[int, int] = (512, 64), border: int = 3, distance_to_top: int = 0):
    textbox_border = pg.Rect(0, 0, *dimension)
    textbox_border.center = screen.get_rect().center
    textbox_border.top = screen.get_rect().top + distance_to_top
    left_x, left_y = textbox_border.topleft
    textbox = pg.Rect(
        0, 0, dimension[0] - border * 2, dimension[1] - border * 2)
    textbox.topleft = (left_x + border, left_y + border)
    return textbox, textbox_border


def create_button(screen: pg.Surface, margin: tuple[int, int]):
    border = 3
    width, height = 512, 64
    center_x, center_y = screen.get_rect().center
    textbox_border = pg.Rect(0, 0, width, height)
    textbox_border.center = (center_x, center_y)
    textbox_border = textbox_border.move(*margin)
    left_x, left_y = textbox_border.topleft
    textbox = pg.Rect(0, 0, width - border * 2, height - border * 2)
    textbox.topleft = (left_x + border, left_y + border)
    return textbox, textbox_border


def create_submit_box():
    dist_from_corner = STYLE["width"] // 40
    box_topright = STYLE["width"] - \
        dist_from_corner, dist_from_corner
    width, height = STYLE["width"] // 6, STYLE["height"] // 13
    box = pg.Rect(0, 0, width, height)
    box.topright = box_topright
    return box


def draw_submit_box(screen: pg.Surface, submit_box: pg.Rect, text: str = "Submit", color: str = "lightblue"):
    pg.draw.rect(screen, color, submit_box)
    font = STYLE["font"]["text"]
    submit_text_surface = font.render(text, True, (0, 0, 0))
    text_rect = submit_text_surface.get_rect(center=submit_box.center)
    screen.blit(submit_text_surface, text_rect)


def create_add_box():
    dist_from_corner = STYLE["width"] // 40
    box_bottomright = STYLE["width"] - \
        dist_from_corner, STYLE["height"] - dist_from_corner
    width, height = STYLE["width"] // 9, STYLE["height"] // 15
    box = pg.Rect(0, 0, width, height)
    box.bottomright = box_bottomright
    return box


def draw_add_box(screen: pg.Surface, add_box: pg.Rect, text: str = "Add", color: str = "lightblue"):
    pg.draw.rect(screen, color, add_box)
    font = STYLE["font"]["text"]
    add_text_surface = font.render(text, True, (0, 0, 0))
    text_rect = add_text_surface.get_rect(center=add_box.center)
    screen.blit(add_text_surface, text_rect)
