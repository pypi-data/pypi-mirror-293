from os import PathLike
from typing import IO

import pygame

from folumo.betterGUI.constants import MOUSEMOTION, BLACK, WHITE
from folumo.betterGUI.screen import Element, Canvas, Main, Color


class Sprite(Element):
    def __init__(self, xy: tuple[int, int],
                 image_path: str | bytes | PathLike[str] | PathLike[bytes] | IO[bytes] | IO[str]):
        super().__init__(xy)
        self.image = pygame.image.load(image_path)

    def render(self) -> Canvas:
        canvas = Canvas(self.image.get_size())
        canvas.surf.blit(self.image, (0, 0))
        return canvas


class AnimatedSprite(Element):
    def __init__(self, xy: tuple[int, int],
                 image_paths: list[str | bytes | PathLike[str] | PathLike[bytes] | IO[bytes] | IO[str]], frame_rate=10):
        super().__init__(xy)
        self.images = [pygame.image.load(path) for path in image_paths]
        self.frame_rate = frame_rate
        self.current_frame = 0
        self.frame_count = 0

    def update(self) -> None:
        self.frame_count += 1
        if self.frame_count >= self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.frame_count = 0

    def render(self) -> Canvas:
        self.update()
        canvas = Canvas(self.images[self.current_frame].get_size())
        canvas.surf.blit(self.images[self.current_frame], (0, 0))
        return canvas


class HealthBar(Element):
    def __init__(self, xy: tuple[int, int], size: tuple[int, int], max_health: int, current_health: int,
                 bar_color: Color, bg_color: Color):
        super().__init__(xy)
        self.size = size
        self.max_health = max_health
        self.current_health = current_health
        self.bar_color = bar_color
        self.bg_color = bg_color

    def set_health(self, health: int) -> None:
        self.current_health = max(0, min(self.max_health, health))

    def render(self) -> Canvas:
        canvas = Canvas(self.size)
        pygame.draw.rect(canvas.surf, self.bg_color.getColor(), (0, 0, *self.size))
        health_width = int(self.size[0] * (self.current_health / self.max_health))
        pygame.draw.rect(canvas.surf, self.bar_color.getColor(), (0, 0, health_width, self.size[1]))
        return canvas


class Inventory(Element):
    def __init__(self, xy: tuple[int, int], size: tuple[int, int], slot_size: int, slot_color: Color,
                 bg_color: Color):
        super().__init__(xy)
        self.size = size
        self.slot_size = slot_size
        self.slot_color = slot_color
        self.bg_color = bg_color
        self.items: list[list[None | Element]] = [[None for _ in range(size[0])] for _ in range(size[1])]

    def add_item(self, item: Element, position: tuple[int, int]) -> None:
        x, y = position
        if 0 <= x < self.size[0] and 0 <= y < self.size[1]:
            self.items[y][x] = item

    def render(self) -> Canvas:
        canvas = Canvas((self.size[0] * self.slot_size, self.size[1] * self.slot_size))
        canvas.surf.fill(self.bg_color)
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                pygame.draw.rect(canvas.surf, self.slot_color.getColor(),
                                 (x * self.slot_size, y * self.slot_size, self.slot_size, self.slot_size), 1)
                item = self.items[y][x]
                if item:
                    item_canvas = item.render()
                    canvas.surf.blit(item_canvas.surf, (x * self.slot_size, y * self.slot_size))
        return canvas


class HUD(Element):
    def __init__(self, xy: tuple[int, int], elements: list[Element]):
        super().__init__(xy)
        self.elements: list[Element] = elements

    def render(self) -> Canvas:
        canvas = Canvas((1920, 1080))
        for element in self.elements:
            element_canvas = element.render()
            canvas.surf.blit(element_canvas.surf, element.xy)
        return canvas


class DialogueBox(Element):
    def __init__(self, xy: tuple[int, int], size: tuple[int, int], text: str, font_size: int = 24,
                 text_color: Color = BLACK, bg_color: Color = WHITE):
        super().__init__(xy)
        self.size = size
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.text_color = text_color
        self.bg_color = bg_color

    def render(self) -> Canvas:
        canvas = Canvas(self.size, False, self.bg_color)
        lines = self.text.split('\n')
        y = 0
        for line in lines:
            text_surface = self.font.render(line, True, self.text_color.getColor())
            canvas.surf.blit(text_surface, (5, y))
            y += text_surface.get_height() + 5
        return canvas


class Timer(Element):
    def __init__(self, xy: tuple[int, int], main: Main, size: tuple[int, int], font_size: int = 24,
                 text_color: Color = WHITE, bg_color: Color = BLACK):
        super().__init__(xy)
        self.size = size
        self.main = main
        self.font = pygame.font.Font(None, font_size)
        self.text_color = text_color
        self.bg_color = bg_color
        self.time_left = 0
        self.running = False

    def start(self, time) -> None:
        self.time_left = time
        self.running = True

    def stop(self) -> None:
        self.running = False

    def update(self) -> None:
        if self.running and self.time_left > 0:
            self.time_left -= 1 / self.main.fps
            if self.time_left <= 0:
                self.time_left = 0
                self.running = False

    def render(self) -> Canvas:
        self.update()
        canvas = Canvas(self.size, False, self.bg_color)
        minutes = int(self.time_left // 60)
        seconds = int(self.time_left % 60)
        time_str = f"{minutes:02}:{seconds:02}"
        text_surface = self.font.render(time_str, True, self.text_color.getColor())
        canvas.surf.blit(text_surface, (
        self.size[0] / 2 - text_surface.get_width() / 2, self.size[1] / 2 - text_surface.get_height() / 2))
        return canvas


class Tooltip(Element):
    def __init__(self, element: Element, text: str, font_size: int = 24, text_color: Color = BLACK,
                 bg_color: Color = WHITE):
        super().__init__(element.xy)
        self.element = element
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.text_color = text_color
        self.bg_color = bg_color
        self.visible = False

    def is_hovering(self, pos: tuple[int, int]) -> bool:
        x, y = self.xy
        width, height = self.element.lastRender.surf.get_size()
        return x <= pos[0] <= x + width and y <= pos[1] <= y + height

    def handle_event(self, event) -> None:
        self.element.handle_event(event)
        if event.type == MOUSEMOTION:
            hovering = self.is_hovering(event.pos)
            self.visible = hovering

    def show(self) -> None:
        self.visible = True

    def hide(self) -> None:
        self.visible = False

    def render(self) -> Canvas:
        if not self.visible:
            return Canvas((0, 0))

        text_surface = self.font.render(self.text, True, self.text_color.getColor())
        canvas = Canvas((text_surface.get_width() + 10, text_surface.get_height() + 10), False, self.bg_color)
        canvas.surf.blit(text_surface, (5, 5))
        return canvas


class Slider(Element):
    def __init__(self, xy, size: tuple[int, int], min_value: int, max_value: int, initial_value: int,
                 bar_color: Color, knob_color: Color):
        super().__init__(xy)
        self.size = size
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.bar_color = bar_color
        self.knob_color = knob_color
        self.knob_position = (initial_value - min_value) / (max_value - min_value) * size[0]
        self.dragging = False

    def handle_event(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovering(event.pos):
                self.dragging = True
                self.update_knob(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.update_knob(event.pos)

    def update_knob(self, pos) -> None:
        x = pos[0] - self.xy[0]
        x = max(0, min(x, self.size[0]))
        self.knob_position = x
        self.value = self.min_value + (self.max_value - self.min_value) * (x / self.size[0])

    def is_hovering(self, pos) -> bool:
        x, y = self.xy
        width, height = self.size
        return x <= pos[0] <= x + width and y <= pos[1] <= y + height

    def render(self) -> Canvas:
        canvas = Canvas(self.size)
        pygame.draw.rect(canvas.surf, self.bar_color.getColor(), (0, self.size[1] // 2 - 5, self.size[0], 10))
        pygame.draw.circle(canvas.surf, self.knob_color.getColor(), (int(self.knob_position), self.size[1] // 2), 10)
        return canvas


class collideManager:
    def __init__(self):
        self.elements: list[Element] = []

    def addElement(self, element: Element) -> None:
        self.elements.append(element)

    def removeElementIndex(self, index: int) -> None:
        del self.elements[index]

    def removeElementObj(self, element: Element) -> bool:
        if element in self.elements:
            self.elements.remove(element)
            return True

        return False

    def isOnGround(self, xy: tuple[int, int], hitbox: tuple[int, int], thisElement: Element) -> tuple[
        bool, Element | None]:
        player_bottom = xy[1] + hitbox[1]

        for element in self.elements:
            if element is thisElement:
                continue

            element_top = element.xy[1]
            element_bottom = element.xy[1] + element.lastRender.surf.get_height()
            element_left = element.xy[0]
            element_right = element.xy[0] + element.lastRender.surf.get_width()

            if (xy[0] < element_right and
                    xy[0] + hitbox[0] > element_left and
                    player_bottom >= element_top and
                    xy[1] < element_bottom):
                return True, element

        return False, None

    def isInWalls(self, xy: tuple[int, int], hitbox: tuple[int, int], thisElement: Element) -> tuple[
        bool, Element | None, str]:
        for element in self.elements:
            if element is thisElement:
                continue

            element_top = element.xy[1]
            element_bottom = element.xy[1] + element.lastRender.surf.get_height()
            element_left = element.xy[0]
            element_right = element.xy[0] + element.lastRender.surf.get_width()

            if (xy[0] < element_right and
                    xy[0] + hitbox[0] > element_left and
                    xy[1] < element_bottom and
                    xy[1] + hitbox[1] > element_top):

                if xy[0] < element_left:
                    return True, element, 'left'
                elif xy[0] + hitbox[0] > element_right:
                    return True, element, 'right'
                elif xy[1] < element_top:
                    return True, element, 'top'
                elif xy[1] + hitbox[1] > element_bottom:
                    return True, element, 'bottom'

        return False, None, ''


class Player(Element):
    def __init__(self, xy: tuple[int, int], size: tuple[int, int], color: Color,
                 colliderManagerObj: collideManager, addToCollideManager=True):
        super().__init__(xy)
        self.size = size
        self.color = color
        self.canvas = Canvas(size, False, color)

        # Movement variables
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.gravity = 0.5
        self.jump_strength = -10
        self.on_ground = True

        # Constants
        self.move_speed = 2
        self.friction = 0.9
        self.colliderManager = colliderManagerObj

        if addToCollideManager:
            self.colliderManager.addElement(self)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:  # Move up
                self.acceleration.y = -self.move_speed
            if event.key == pygame.K_s:  # Move down
                self.acceleration.y = self.move_speed
            if event.key == pygame.K_a:  # Move left
                self.acceleration.x = -self.move_speed
            if event.key == pygame.K_d:  # Move right
                self.acceleration.x = self.move_speed
            if event.key == pygame.K_SPACE and self.on_ground:  # Jump
                self.velocity.y = self.jump_strength
                self.on_ground = False

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                self.acceleration.y = 0
            if event.key in (pygame.K_a, pygame.K_d):
                self.acceleration.x = 0

    def update(self):
        # Apply acceleration
        self.velocity += self.acceleration
        self.velocity.y += self.gravity

        # Apply friction
        self.velocity.x *= self.friction

        # Update position
        new_x = self.xy[0] + int(self.velocity.x)
        new_y = self.xy[1] + int(self.velocity.y)

        check, obj, direction = self.colliderManager.isInWalls((new_x, new_y), self.canvas.surf.get_size(), self)

        if check and obj is not None:
            if direction == 'left':
                new_x = obj.xy[0] - self.size[0]
            elif direction == 'right':
                new_x = obj.xy[0] + obj.lastRender.surf.get_width()
            elif direction == 'top':
                new_y = obj.xy[1] - self.size[1]
            elif direction == 'bottom':
                new_y = obj.xy[1] + obj.lastRender.surf.get_height()

            self.velocity.x = 0

        check, obj = self.colliderManager.isOnGround((new_x, new_y), self.canvas.surf.get_size(), self)

        if check and obj is not None:
            self.velocity.y = 0
            self.on_ground = True
            new_y = obj.xy[1] - self.size[1]
        else:
            self.on_ground = False

        self.xy = (new_x, new_y)

    def render(self) -> Canvas:
        self.update()
        return self.canvas
