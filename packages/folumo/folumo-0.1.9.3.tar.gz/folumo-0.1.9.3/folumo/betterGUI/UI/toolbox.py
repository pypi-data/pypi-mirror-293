import pygame

from folumo.betterGUI.screen import Element, Canvas, Color
from folumo.betterGUI.constants import MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP, WHITE, BLACK


class Button(Element):
    def __init__(self, xy, canvasNormal: Canvas, canvasHover: Canvas, canvasDown: Canvas, onLeftDown=None, onLeftUp=None, onRightDown=None, onRightUp=None, onHover=None):
        super().__init__(xy)

        self.normalCanvas = canvasNormal
        self.hoverCanvas = canvasHover
        self.downCanvas = canvasDown

        self.isHovering = False
        self.isDown = False

        self.onHover_ = onHover
        self.onLeftDown_ = onLeftDown
        self.onLeftUp_ = onLeftUp
        self.onRightDown_ = onRightDown
        self.onRightUp_ = onRightUp

    def onHover(self, hovering):
        self.isHovering = hovering
        if self.onHover_:
            self.onHover_(hovering)

    def onLeftDown(self):
        self.isDown = True
        if self.onLeftDown_:
            self.onLeftDown_()

    def onLeftUp(self):
        self.isDown = False
        if self.onLeftUp_:
            self.onLeftUp_()

    def onRightDown(self):
        self.isDown = True
        if self.onRightDown_:
            self.onRightDown_()

    def onRightUp(self):
        self.isDown = False
        if self.onRightUp_:
            self.onRightUp_()

    def handle_event(self, event):
        if event.type == MOUSEMOTION:
            hovering = self.is_hovering(event.pos)
            if hovering != self.isHovering:
                self.onHover(hovering)
        elif event.type == MOUSEBUTTONDOWN:
            if self.is_hovering(event.pos):
                if event.button == 1:
                    self.onLeftDown()
                elif event.button == 3:
                    self.onRightDown()
        elif event.type == MOUSEBUTTONUP:
            if self.isDown and self.is_hovering(event.pos):
                if event.button == 1:
                    self.onLeftUp()
                elif event.button == 3:
                    self.onRightUp()

    def is_hovering(self, pos):
        x, y = self.xy
        width, height = self.normalCanvas.surf.get_size()
        return x <= pos[0] <= x + width and y <= pos[1] <= y + height

    def render(self) -> Canvas:
        if self.isDown:
            return self.downCanvas
        elif self.isHovering:
            return self.hoverCanvas
        else:
            return self.normalCanvas


class Slider(Element):
    def __init__(self, xy, wh, min_val, max_val, current_val, color: Color, handle_color, on_change=None):
        super().__init__(xy)
        self.wh = wh
        self.min_val = min_val
        self.max_val = max_val
        self.current_val = current_val
        self.color = color
        self.handle_color = handle_color
        self.on_change = on_change
        self.dragging = False

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and self.is_hovering(event.pos):
            self.dragging = True
        elif event.type == MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == MOUSEMOTION and self.dragging:
            self.current_val = self.get_value_from_pos(event.pos)

            if self.on_change:
                self.on_change(self.current_val)

    def is_hovering(self, pos):
        x, y = self.xy
        return x <= pos[0] <= x + self.wh[0] and y <= pos[1] <= y + self.wh[1]

    def get_value_from_pos(self, pos):
        x = self.xy[0]
        rel_x = pos[0] - x
        return self.min_val + (rel_x / self.wh[0]) * (self.max_val - self.min_val)

    def render(self) -> Canvas:
        newCanvas = Canvas(self.wh, True)
        pygame.draw.rect(newCanvas.surf, self.color.getColor(), (0, self.wh[1] // 2 - 2, self.wh[0], 4))

        handle_x = int((self.current_val - self.min_val) / (self.max_val - self.min_val) * self.wh[0])
        pygame.draw.circle(newCanvas.surf, self.handle_color, (handle_x, self.wh[1] // 2), 10)

        return newCanvas


class ToggleSwitch(Element):
    def __init__(self, xy, wh, is_on, color_on: Color, color_off: Color, handle_color: Color, on_toggle=None):
        super().__init__(xy)
        self.wh = wh
        self.is_on = is_on
        self.color_on = color_on
        self.color_off = color_off
        self.handle_color = handle_color
        self.on_toggle = on_toggle

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and self.is_hovering(event.pos):
            self.is_on = not self.is_on

            if self.on_toggle:
                self.on_toggle(self.is_on)

    def is_hovering(self, pos):
        x, y = self.xy
        return x <= pos[0] <= x + self.wh[0] and y <= pos[1] <= y + self.wh[1]

    def render(self) -> Canvas:
        newCanvas = Canvas(self.wh, True)
        color = self.color_on if self.is_on else self.color_off
        pygame.draw.rect(newCanvas.surf, color.getColor(), (0, 0, self.wh[0], self.wh[1]), border_radius=15)

        handle_x = self.wh[0] - self.wh[1] if self.is_on else 0
        pygame.draw.circle(newCanvas.surf, self.handle_color.getColor(), (handle_x + self.wh[1] // 2, self.wh[1] // 2),
                           self.wh[1] // 2)

        return newCanvas


class ProgressBar(Element):
    def __init__(self, xy, wh, min_val, max_val, current_val, bar_color: Color, bg_color: Color):
        super().__init__(xy)
        self.wh = wh
        self.min_val = min_val
        self.max_val = max_val
        self.current_val = current_val
        self.bar_color = bar_color
        self.bg_color = bg_color

    def update(self, new_val):
        self.current_val = new_val

    def render(self) -> Canvas:
        newCanvas = Canvas(self.wh, True)
        pygame.draw.rect(newCanvas.surf, self.bg_color.getColor(), (0, 0, self.wh[0], self.wh[1]))

        bar_width = int((self.current_val - self.min_val) / (self.max_val - self.min_val) * self.wh[0])
        pygame.draw.rect(newCanvas.surf, self.bar_color.getColor(), (0, 0, bar_width, self.wh[1]))

        return newCanvas


class DraggableElement(Element):
    def __init__(self, element: Element):
        super().__init__(element.xy)
        self.element = element
        self.dragging = False
        self.offset = (0, 0)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovering(event.pos):
                self.dragging = True
                self.offset = (self.xy[0] - event.pos[0], self.xy[1] - event.pos[1])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.xy = (event.pos[0] + self.offset[0], event.pos[1] + self.offset[1])

    def is_hovering(self, pos):
        x, y = self.xy
        width, height = self.element.render().surf.get_size()
        return x <= pos[0] <= x + width and y <= pos[1] <= y + height

    def render(self) -> Canvas:
        self.element.xy = self.xy
        return self.element.render()


class ListElement(Element):
    def __init__(self, xy, elements: list[Element], viewport_size: tuple[int, int], spacing: int = 5):
        super().__init__(xy)
        self.elements = elements
        self.viewport_size = viewport_size
        self.spacing = spacing
        self.scroll_offset = 0
        self.total_height = sum(el.render().surf.get_height() for el in elements) + spacing * (len(elements) - 1)

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset += event.y * 10  # Scroll speed
            self.scroll_offset = max(min(self.scroll_offset, 0), self.viewport_size[1] - self.total_height)

    def render(self) -> Canvas:
        canvas = Canvas(self.viewport_size)
        y_offset = self.scroll_offset

        for element in self.elements:
            element_canvas = element.render()
            canvas.surf.blit(element_canvas.surf, (0, y_offset))
            y_offset += element_canvas.surf.get_height() + self.spacing

        return canvas


class InputElement(Element):
    def __init__(self, xy, size: tuple[int, int], input_type='normal'):
        super().__init__(xy)
        self.size = size
        self.input_type = input_type
        self.textShow = ''
        self.text = ''
        self.active = False
        self.font = pygame.font.Font(None, 24)
        self.bg_color = WHITE
        self.text_color = BLACK
        self.border_color = BLACK
        self.cursor_visible = True
        self.cursor_counter = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovering(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.textShow = self.textShow[:-1]
                self.text = self.text[:-1]
            elif event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL):
                clipboard_text = pygame.scrap.get(pygame.SCRAP_TEXT).decode('utf-8')[:-1]
                if self.input_type == 'number':
                    clipboard_text = ''.join(filter(str.isdigit, clipboard_text))
                self.textShow += clipboard_text
                self.text += clipboard_text
            else:
                if not event.unicode.isprintable():
                    return

                if self.input_type == 'number' and not event.unicode.isdigit():
                    return

                if self.input_type == 'password':
                    self.textShow += '*'
                else:
                    self.textShow += event.unicode

                self.text += event.unicode

    def is_hovering(self, pos):
        x, y = self.xy
        width, height = self.size
        return x <= pos[0] <= x + width and y <= pos[1] <= y + height

    def render(self) -> Canvas:
        canvas = Canvas(self.size, False, self.bg_color)
        pygame.draw.rect(canvas.surf, self.border_color.getColor(), (0, 0, *self.size), 2)

        display_text = self.textShow if self.input_type != 'password' else '*' * len(self.textShow)
        text_surface = self.font.render(display_text, True, self.text_color.getColor())
        canvas.surf.blit(text_surface, (5, (self.size[1] - text_surface.get_height()) // 2))

        # Handle cursor blinking
        self.cursor_counter = (self.cursor_counter + 1) % 60
        if self.active and self.cursor_counter < 30:
            cursor_x = text_surface.get_width() + 5
            pygame.draw.line(canvas.surf, self.text_color.getColor(), (cursor_x, 5), (cursor_x, self.size[1] - 5), 2)

        return canvas


class Menu(Element):
    def __init__(self, xy, options: list[str], font_size=24, bg_color=BLACK, text_color=WHITE):
        super().__init__(xy)
        self.options = options
        self.font = pygame.font.Font(None, font_size)
        self.bg_color = bg_color
        self.text_color = text_color
        self.selected_option = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for index, option_rect in enumerate(self.option_rects):
                if option_rect.collidepoint(mouse_pos):
                    self.selected_option = self.options[index]

    def render(self) -> Canvas:
        canvas = Canvas((max(self.font.size(option)[0] for option in self.options) + 20,
                         sum(self.font.size(option)[1] for option in self.options) + 20), False, self.bg_color)
        self.option_rects = []
        y = 10
        for option in self.options:
            text_surface = self.font.render(option, True, self.text_color.getColor())
            canvas.surf.blit(text_surface, (10, y))
            self.option_rects.append(pygame.Rect(10, y, text_surface.get_width(), text_surface.get_height()))
            y += text_surface.get_height() + 10
        return canvas
