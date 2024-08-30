import pygame

from folumo.betterGUI.screen import Element, Canvas, Color
from functools import lru_cache
import requests
from io import BytesIO


class Rect(Element):
    def __init__(self, xy, wh, color: Color):
        super().__init__(xy)

        self.wh = wh
        self.color = color

    def render(self) -> Canvas:
        aLen = len(self.color.getColor())
        newCanvas = Canvas(self.wh, aLen == 4, self.color)
        return newCanvas


class Circle(Element):
    def __init__(self, xy, radius, color: Color):
        super().__init__(xy)
        self.radius = radius
        self.color = color

    def render(self) -> Canvas:
        diameter = self.radius * 2
        newCanvas = Canvas((diameter, diameter), True)
        pygame.draw.circle(newCanvas.surf, self.color.getColor(), (self.radius, self.radius), self.radius)
        return newCanvas


class Line(Element):
    def __init__(self, start_pos, end_pos, color: Color, width=1):
        super().__init__(start_pos)
        self.end_pos = end_pos
        self.color = color
        self.width = width

    def render(self) -> Canvas:
        width = max(self.xy[0], self.end_pos[0])
        height = max(self.xy[1], self.end_pos[1])
        newCanvas = Canvas((width, height), True)
        pygame.draw.line(newCanvas.surf, self.color.getColor(), self.xy, self.end_pos, self.width)
        return newCanvas


class Text(Element):
    def __init__(self, xy, text, font_name, font_size, color: Color):
        super().__init__(xy)
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(self.font_name, self.font_size)

    def render(self) -> Canvas:
        text_surf = self.font.render(self.text, True, self.color.getColor())
        newCanvas = Canvas(text_surf.get_size(), True)
        newCanvas.surf.blit(text_surf, (0, 0))
        return newCanvas


class Image(Element):
    def __init__(self, xy, path, isWeb=False):
        super().__init__(xy)
        self.path = path
        self.isWeb = isWeb

    def render(self) -> Canvas:
        return loadImage(self.path, self.isWeb)


@lru_cache()
def loadImage(path, isWeb=False) -> "Canvas":
    if isWeb:
        response = requests.get(path)
        if response.status_code == 200:
            image_data = BytesIO(response.content)
            image = pygame.image.load(image_data)
        else:
            raise ValueError(f"Could not load image from {path}, status code: {response.status_code}")
    else:
        image = pygame.image.load(path)

    canvas = Canvas(image.get_size())
    canvas.surf = image

    return canvas
