import time

import pygame

from constants import WINDOW_WIDTH, MAX_LIVES, SECONDS_PER_LIFE


class TopBar:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("font", 25)

        self.bar = pygame.Rect((0, 0), (WINDOW_WIDTH, 50))
        self.border_thickness = 4
        self.border = pygame.Rect((0, 50 - self.border_thickness),
                                  (WINDOW_WIDTH, self.border_thickness))
        self.life_image = pygame.image.load('assets/life.png')
        self.life_image = pygame.transform.scale(
            self.life_image,
            (100, 100)
        )
        self.lives_display_text = self.font.render(str(self.game.lives), True, 'White')
        self.lives_recharge_rect = pygame.Rect((28, 11),
                                               (75, 30))
        self.lives_recharge_text = self.font.render("text", True, 'White')

    def draw(self, screen: pygame.Surface):
        self.lives_display_text = self.font.render(str(self.game.lives), True, 'White')
        self.lives_recharge_text = self.font.render(self.get_life_recharge_text(), True, 'White')

        pygame.draw.rect(screen, color='#f1b941', rect=self.bar)
        pygame.draw.rect(screen, color='#f6d388', rect=self.border)
        pygame.draw.rect(screen, color='#f8dca0', rect=self.lives_recharge_rect, border_radius=10)
        screen.blit(self.life_image, (-20, -25))
        screen.blit(self.lives_display_text, (25, 17))
        screen.blit(self.lives_recharge_text, (55, 17))

    def get_life_recharge_text(self):
        if self.game.lives == MAX_LIVES:
            return 'Full'
        else:
            current_time = int(time.time())
            remaining_time = current_time - self.game.last_life_gain_timestamp
            if remaining_time >= SECONDS_PER_LIFE:
                self.game.increase_lives()
            display_time = SECONDS_PER_LIFE - remaining_time
            formatted_time = f'{str(display_time // 60)}:{(display_time % 60):02d}'
            return formatted_time
