import pygame

from common.button import Button
from common.topbar import TopBar
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, INACTIVE_LEVELS_COLORS, \
    PASSED_LEVELS_COLOR, CURRENT_LEVEL_COLOR


class LevelsScreen:

    def __init__(self, game):
        self.game = game
        self.background = pygame.image.load('assets/levels_screen_background.webp')
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.top_bar = TopBar(game)

        self.right_img = pygame.image.load('assets/arrow.png')
        self.left_img = pygame.transform.rotate(pygame.image.load('assets/arrow.png'), 180)

        self.levels_distance = 100
        self.levels_move = 0
        self.level_button_width = 60

        self.right = Button(
            image=self.right_img,
            on_action=lambda: self.set_levels_move(-self.levels_distance),
            pos=(WINDOW_WIDTH - 100, WINDOW_HEIGHT - 250),
            width=50, height=50
        )
        self.left = Button(
            image=self.left_img,
            on_action=lambda: self.set_levels_move(self.levels_distance),
            pos=(50, WINDOW_HEIGHT - 250),
            width=50,
            height=50
        )
        self.levels_buttons = []
        for level in range(len(self.game.levels_info)):
            button_x = (level - self.game.current_max_level) * self.levels_distance \
                       + WINDOW_WIDTH / 2 - self.level_button_width
            button = Button(
                text=str(level + 1),
                width=self.level_button_width,
                height=50,
                on_action=lambda lvl=level: self.start_level(lvl),
                pos=(button_x, WINDOW_HEIGHT - 150)
            )
            self.levels_buttons.append(button)

    def display(self) -> None:
        screen = self.game.screen
        while self.game.current_screen == 'levels_screen':
            screen.blit(self.background, (0, 0))
            self.top_bar.draw(screen)
            self.left.draw(screen)
            self.right.draw(screen)
            for index, button in enumerate(self.levels_buttons):
                self.move_button_if_needed(button)
                button.active = index <= self.game.current_max_level
                if index == self.game.current_max_level:
                    button.set_colors(CURRENT_LEVEL_COLOR)
                elif index < self.game.current_max_level:
                    button.set_colors(PASSED_LEVELS_COLOR)
                else:
                    button.set_colors(INACTIVE_LEVELS_COLORS)
                button.draw(screen)
            self.game.check_for_quit()
            pygame.display.update()
            self.game.fps_clock.tick(FPS)

    def move_button_if_needed(self, button: Button) -> None:
        if self.levels_move != 0:
            if self.levels_move > 0:
                button.move(4, 0)
                self.levels_move -= 1
            else:
                button.move(-4, 0)
                self.levels_move += 1

    def set_levels_move(self, move: int) -> None:
        if self.levels_move == 0:
            self.levels_move = move

    def start_level(self, level: int) -> None:
        if self.game.lives == 0:
            return
        if level > self.game.current_max_level:
            return
        self.game.level_to_play = level
        self.game.set_screen('game_screen')
