import pygame

from constants import *
from entry_screen.entry_screen import EntryScreen
from game_screen.game_screen import GameScreen
from levels_screen.levels_screen import LevelsScreen


class CandyCrush:
    def __init__(self):
        pygame.init()
        self.current_screen = "game_screen"
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.fps_clock = pygame.time.Clock()
        self.entry_screen = EntryScreen(self)
        self.levels_screen = LevelsScreen(self)
        self.game_screen = GameScreen(self)

    def set_screen(self, screen: str):
        self.current_screen = screen

    def run(self):
        pygame.display.set_caption("Candy crush")

        while True:
            if self.current_screen == "entry_screen":
                self.entry_screen.display()
            elif self.current_screen == "levels_screen":
                self.levels_screen.display()
            elif self.current_screen == "game_screen":
                self.game_screen.start_game(moves=20)
            self.check_for_quit()
            pygame.display.update()
            self.fps_clock.tick(FPS)

    def check_for_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

