from typing import Literal, TypedDict
import os
import pygame

current_dir = os.path.basename(os.getcwd())
if current_dir == "src":
    BASE = os.path.join(os.path.abspath(os.getcwd()), "static", "font")
else:
    BASE = os.path.join(os.path.abspath(os.getcwd()), "src", "static", "font")

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


class ColorType(TypedDict):
    active: pygame.Color
    default: pygame.Color


class StyleType(TypedDict):
    width: int
    height: int
    font: FontType
    fps: int
    box_colors: list[ColorType]


STYLE: StyleType = {
    "font": {
        "title": font_builder(72, "extrabold"),
        "question": font_builder(36, "bold"),
        "answer": font_builder(24, "extrabold"),
        "text": font_builder(16)
    },
    "height": 720,
    "width": 1280,
    "fps": 60,
    "box_colors": [
        # Red
        {"active": pygame.Color("#913831"), "default": "red"},
        # Green
        {"active": pygame.Color("#097969"),
         "default": pygame.Color("#5F9EA0")},
        # Blue
        {"active": pygame.Color("#00008B"),
         "default": pygame.Color("#A7C7E7")},
        # Yellow
        {"active": pygame.Color("#FFD700"), "default": pygame.Color("#FCF55F")}
    ]
}
