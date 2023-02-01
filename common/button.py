from typing import Any

import pygame.draw
from pygame import font


class Button:

    def __init__(self, text, on_action, pos, width, height, primary_color, secondary_color, tertiary_color):  # add elevation?
        self.pressed = False
        self.elevation = 6
        self.dynamic_elevation = self.elevation
        self.original_y_pos = pos[1]
        self.on_action = on_action

        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.tertiary_color = tertiary_color

        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = primary_color

        self.bottom_rect = pygame.Rect(pos, (width, self.elevation))
        self.bottom_color = tertiary_color

        self.font = pygame.font.SysFont("font", 25)
        self.text_surface = self.font.render(text, True, 'White')
        self.text_rect = self.text_surface.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=20)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=20)
        screen.blit(self.text_surface, self.text_rect)
        self.is_pressed()

    def is_pressed(self):
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
