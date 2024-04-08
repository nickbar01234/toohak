from typing import Literal, TypedDict
import pygame

BASE = "./static/font"


# pylint: disable=E1101
pygame.init()


def font_builder(size: int, sty: Literal["default", "black", "bold", "extrabold"] = "black"):
    path = {
        "default": f"{BASE}/Montserrat-VariableFont_wght.ttf",
        "black": f"{BASE}/Montserrat-Black.ttf",
        "bold": f"{BASE}/Montserrat-Bold.ttf",
        "extrabold": f"{BASE}/Montserrat-ExtraBold.ttf"
    }
    return pygame.font.Font(path[sty], size)


class FontType(TypedDict):
    title: pygame.font.Font
    question: pygame.font.Font
    answer: pygame.font.Font
    text: pygame.font.Font


class StyleType(TypedDict):
    width: int
    height: int
    font: FontType
    fps: int


STYLE: StyleType = {
    "font": {
        "title": font_builder(72, "extrabold"),
        "question": font_builder(36, "bold"),
        "answer": font_builder(24, "extrabold"),
        "text": font_builder(16)
    },
    "width": 720,
    "height": 1280,
    "fps": 60
}
