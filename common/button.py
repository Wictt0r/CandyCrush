from typing import Tuple

import pygame.draw

from constants import INACTIVE_LEVELS_COLORS


class Button:

    def __init__(self, text=None, image=None, on_action=lambda: None, pos=(0, 0), width: int = 0,
                 height: int = 0,
                 colors: Tuple[str, str, str] = INACTIVE_LEVELS_COLORS):
        self.pressed = False
        self.active = True
        self.elevation = 6
        self.dynamic_elevation = self.elevation
        self.pos = pos
        self.on_action = on_action

        self.primary_color = colors[0]
        self.secondary_color = colors[1]
        self.tertiary_color = colors[2]

        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = colors[0]

        self.bottom_rect = pygame.Rect(pos, (width, self.elevation))
        self.bottom_color = colors[2]

        self.image = pygame.transform.scale(image, (width - 10, height - 10)) \
            if image is not None else None

        self.font = pygame.font.SysFont("font", 25)
        self.text_surface = self.font.render(text, True, 'White')
        self.text_rect = self.text_surface.get_rect(center=self.top_rect.center)

    def draw(self, screen: pygame.Surface) -> None:
        self.top_rect.y = self.pos[1] - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=20)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=20)

        if self.text_surface is not None:
            screen.blit(self.text_surface, self.text_rect)
        if self.image is not None:
            screen.blit(self.image,
                        dest=(self.pos[0] + 4, self.pos[1] - self.dynamic_elevation + 5))
        if self.active:
            self.is_pressed()

    def is_pressed(self) -> None:
        mouse_position = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_position):
            self.top_color = self.secondary_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    self.on_action()
                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = self.primary_color
            self.pressed = False

    def move(self, x: int, y: int):
        self.pos = (self.pos[0] + x, self.pos[1] + y)
        self.top_rect.center = self.pos
        self.bottom_rect.center = self.pos

    def set_colors(self, colors: Tuple[str, str, str]):
        self.primary_color = colors[0]
        self.secondary_color = colors[1]
        self.tertiary_color = colors[2]
        self.bottom_color = colors[2]
