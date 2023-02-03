import pygame

from common.button import Button
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS


class EntryScreen:

    def __init__(self, candy_crush):
        self.game = candy_crush
        self.background = pygame.image.load('assets/entry_screen_background.jpg')
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.play_button = Button(
            text="Play",
            on_action=lambda: self.game.set_screen("levels_screen"),
            pos=(WINDOW_WIDTH / 2 - 50, 400),
            width=100,
            height=50,
            colors=('#168823', '#207e2b', '#2f6f36')
        )
        self.quit_button = Button(
            text="Quit",
            on_action=lambda: pygame.quit(),
            pos=(WINDOW_WIDTH / 2 - 50, 480),
            width=100,
            height=50,
            colors=('#f09133', '#d97a1c', '#c0752a')
        )

    def display(self):
        screen = self.game.screen
        while self.game.current_screen == 'entry_screen':
            screen.blit(self.background, (0, 0))
            self.play_button.draw(screen)
            self.quit_button.draw(screen)
            self.game.check_for_quit()
            pygame.display.update()
            self.game.fps_clock.tick(FPS)
