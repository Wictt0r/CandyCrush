import pygame

from common.button import Button
from common.topbar import TopBar
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS


class LevelsScreen:

    def __init__(self, game):
        self.game = game
        self.background = pygame.image.load('assets/levels_screen_background.webp')
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.top_bar = TopBar(game)

        self.right_img = pygame.image.load('assets/arrow.png')
        self.left_img = pygame.transform.rotate(pygame.image.load('assets/arrow.png'), 180)

        self.levels_distance = 75
        self.levels_move = 0
        self.level_button_width = 50

        self.right = Button(
            image=self.right_img,
            on_action=lambda: self.set_levels_move(self.levels_distance),
            pos=(WINDOW_WIDTH - 100, 350),
            width=50, height=50
        )
        self.left = Button(
            image=self.left_img,
            on_action=lambda: self.set_levels_move(-self.levels_distance),
            pos=(50, 350),
            width=50,
            height=50
        )
        self.levels_buttons = [
            Button(
                text=str(level + 1),
                width=self.level_button_width,
                height=50,
                on_action=lambda level=level: self.start_level(level),
                pos=(
                    (
                            level - self.game.current_max_level) * self.levels_distance + WINDOW_WIDTH / 2 - self.level_button_width,
                    450)
            )
            for level in range(len(self.game.levels_info))]

    def display(self):
        screen = self.game.screen
        while self.game.current_screen == 'levels_screen':
            screen.blit(self.background, (0, 0))
            self.top_bar.draw(screen)
            self.left.draw(screen)
            self.right.draw(screen)
            for button in self.levels_buttons:
                self.move_button_if_needed(button)
                button.draw(screen)
            self.game.check_for_quit()
            pygame.display.update()
            self.game.fps_clock.tick(FPS)

    def move_button_if_needed(self, button: Button):
        if self.levels_move != 0:
            if self.levels_move > 0:
                button.move(4, 0)
                self.levels_move -= 1
            else:
                button.move(-4, 0)
                self.levels_move += 1

    def set_levels_move(self, move: int):
        if self.levels_move == 0:
            self.levels_move = move

    def start_level(self, level):
        if self.game.lives == 0:
            return
        if level > self.game.current_max_level:
            return
        self.game.level_to_play = level
        self.game.set_screen('game_screen')
