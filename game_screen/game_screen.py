import pygame

from constants import FPS


class GameScreen:

    def __init__(self, game):
        self.game = game

    def start_game(self):
        while True:
            self.game.check_for_quit()
            pygame.display.update()
            self.game.fps_clock.tick(FPS)

