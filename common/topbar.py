import pygame

from constants import WINDOW_WIDTH


class TopBar:
    def __init__(self):
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
        self.lives = 5
        self.lives_display_text = self.font.render(str(self.lives), True, 'White')
        self.lives_recharge_rect = pygame.Rect((28, 11),
                                               (75, 30))
        self.lives_recharge_text = self.font.render("text", True, 'White')

    def draw(self, screen: pygame.Surface):
        self.lives_display_text = self.font.render(str(self.lives), True, 'White')
        self.lives_recharge_text = self.font.render("text", True, 'White')

        pygame.draw.rect(screen, color='#f1b941', rect=self.bar)
        pygame.draw.rect(screen, color='#f6d388', rect=self.border)
        pygame.draw.rect(screen, color='#f8dca0', rect=self.lives_recharge_rect, border_radius=10)
        screen.blit(self.life_image, (-20, -25))
        screen.blit(self.lives_display_text, (25, 17))
        screen.blit(self.lives_recharge_text, (55, 17))
