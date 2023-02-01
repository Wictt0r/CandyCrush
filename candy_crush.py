import pygame

from common.button import Button
from constants import *


def entry_screen(screen):
    background = pygame.image.load('assets/entry_screen_background.jpg')
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

    play_button = Button("Play", lambda: None, (WINDOW_WIDTH / 2 - 50, 400), 100, 50, '#168823', '#207e2b', '#2f6f36')
    quit_button = Button("Quit", lambda: pygame.quit(), (WINDOW_WIDTH / 2 - 50, 480), 100, 50, '#f09133', '#f09133', '#c0752a')

    while True:
        screen.blit(background, (0, 0))
        play_button.draw(screen)
        quit_button.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


def levels_screen():
    pass


def game_screen():
    pass


def run_candy_crush():
    pygame.init()
    pygame.display.set_caption("Candy crush")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    current_screen = "entry_screen"
    while True:
        if current_screen == "entry_screen":
            entry_screen(screen)
        elif current_screen == "levels_screen":
            levels_screen()
        elif current_screen == "game_screen":
            game_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
