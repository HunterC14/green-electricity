# components.py

import pygame
from pygame import Surface, Rect
from typing import Optional
from settings import *

class Component:
    def draw(self, surface: Surface, rect: Rect) -> None:
        pass

    def update(self) -> None:
        pass

class Wire(Component):
    def __init__(self) -> None:
        self.powered: bool = False

    def draw(self, surface: Surface, rect: Rect) -> None:
        color: Color = LIGHT_GREEN if self.powered else DARK_GREEN
        pygame.draw.rect(surface, color, rect)

    def update(self) -> None:
        pass  # Logic handled in Grid

class Lever(Component):
    def __init__(self) -> None:
        self.on: bool = False

    def toggle(self) -> None:
        self.on = not self.on

    def draw(self, surface: Surface, rect: Rect) -> None:
        half_height: int = rect.height // 2
        top_rect: Rect = Rect(rect.x, rect.y, rect.width, half_height)
        bottom_rect: Rect = Rect(rect.x, rect.y + half_height, rect.width, half_height)

        if self.on:
            top_color: Color = BROWN
            bottom_color: Color = LIGHT_GRAY
        else:
            top_color: Color = LIGHT_GRAY
            bottom_color: Color = BROWN

        pygame.draw.rect(surface, top_color, top_rect)
        pygame.draw.rect(surface, bottom_color, bottom_rect)

class Lightbulb(Component):
    def __init__(self) -> None:
        self.powered: bool = False

    def draw(self, surface: Surface, rect: Rect) -> None:
        color: Color = LIGHT_GRAY if self.powered else DARK_GRAY
        center: Tuple[int, int] = rect.center
        radius: int = rect.width // 2 - 5
        pygame.draw.circle(surface, color, center, radius)
