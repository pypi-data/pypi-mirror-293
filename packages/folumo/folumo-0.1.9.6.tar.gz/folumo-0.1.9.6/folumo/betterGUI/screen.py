from typing import Type

import pygame
from uuid import uuid4

from pygame import SRCALPHA, QUIT, FULLSCREEN


class Color:
    def __init__(self, r: int, g: int, b: int, a: int | None = None):
        self.rgb = r, g, b
        self.alpha = a

    def getColor(self):
        if self.alpha is None:
            return self.rgb

        r, g, b = self.rgb
        return r, g, b, self.alpha


class Element:
    def __init__(self, xy):
        self.xy = xy
        self.lastRender = Canvas((0, 0))
        self.parent: Element | None = None

    def onCreate(self):
        pass

    def onDestroy(self):
        pass

    def handle_event(self, event) -> bool:
        pass

    def render(self) -> "Canvas":
        return Canvas((0, 0))


class Canvas:
    def __init__(self, wh: tuple[int, int], alpha: int = True, defaultColor: Color | None = None):

        if alpha:
            self.surf = pygame.surface.Surface(wh, SRCALPHA)
        else:
            self.surf = pygame.surface.Surface(wh)

        if defaultColor is not None:
            self.surf.fill(defaultColor.getColor())

    def drawOn(self, element: Element):
        renderResult = element.render()
        element.lastRender = renderResult
        self.surf.blit(renderResult.getPygameSurf(), element.xy)

    def drawFromCanvas(self, canvas: "Canvas", xy):
        self.surf.blit(canvas.getPygameSurf(True), xy)

    def drawFromSurface(self, surface: pygame.Surface, xy):
        self.surf.blit(surface, xy)

    def getPygameSurf(self, getCopy=False):
        if getCopy:
            return self.surf.copy()

        return self.surf

    def getCopy(self):
        canvas = Canvas(self.surf.get_size())
        canvas.drawFromSurface(self.getPygameSurf(), (0, 0))
        return canvas


class Screen:
    def __init__(self, main):
        self.main: Main = main
        self.always = {}

    def add(self, obj):
        uuid = uuid4()

        self.always[uuid] = obj

        return uuid

    def get(self, uuid):
        if uuid in self.always:
            return self.always[uuid]

    def remove(self, uuid):
        if uuid in self.always:
            del self.always[uuid]

    def procesEvent(self, event):
        if event.type == QUIT:
            self.main.running = False

        loopList = list(self.always.values()).copy()
        loopList.reverse()

        for element in loopList:
            if element.handle_event(event):
                break

    def render(self, toRender: Canvas):
        for a in list(self.always.values()).copy():
            toRender.drawOn(a)

    def setAttr(self, name, value):
        pass

    def deactivated(self):
        pass

    def activated(self):
        pass


class Main:
    def __init__(self, screenInfo: dict, screens: dict[str, Type[Screen]], default="main"):
        pygame.init()
        pygame.font.init()

        wh = screenInfo.get("wh", (1920, 1080))
        fullscreen = screenInfo.get("fullscreen", True)
        title = screenInfo.get("title", "")
        os = screenInfo.get("os", None)
        icon = screenInfo.get("icon", "")
        fps = screenInfo.get("fps", 60)

        if fullscreen:
            self.screen = pygame.display.set_mode(wh, FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(wh)

        if icon:
            pygame.display.set_icon(pygame.image.load(icon))

        pygame.display.set_caption(title)
        self.compatOS = os

        self.clock = pygame.time.Clock()

        pygame.scrap.init()

        #self.font = pygame.font.SysFont(None, 24)

        self.wh = wh
        self.running = True
        self.fps = fps
        self.delta = 0
        self.screens = {}
        self.thisScreen = default

        for name, obj in screens.items():
            self.screens[name] = obj(self)

        self.run()

        pygame.quit()
        pygame.font.quit()

    def getScreen(self):
        return self.screens[self.thisScreen]

    def switchScreen(self, screenId):
        if screenId in self.screens:
            self.getScreen().deactivated()
            self.thisScreen = screenId
            self.getScreen().activated()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.getScreen().procesEvent(event)

                if not self.running:
                    return

            self.screen.fill((0, 0, 0))

            newCanvas = Canvas(self.wh)

            self.getScreen().render(newCanvas)

            self.screen.blit(newCanvas.surf, (0, 0))

            pygame.display.update()

            self.delta = self.clock.tick(self.fps)

