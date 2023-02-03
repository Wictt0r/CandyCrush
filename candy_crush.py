import pygame

from common.button import Button
from common.topbar import TopBar
from constants import *

current_screen = "levels_screen"


def entry_screen(screen):
    background = pygame.image.load('assets/entry_screen_background.jpg')
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

    play_button = Button(text="Play", on_action=lambda: set_screen("levels_screen"), pos=(WINDOW_WIDTH / 2 - 50, 400),
                         width=100,
                         height=50,
                         colors=('#168823', '#207e2b', '#2f6f36'))
    quit_button = Button(text="Quit", on_action=lambda: pygame.quit(), pos=(WINDOW_WIDTH / 2 - 50, 480),
                         width=100,
                         height=50,
                         colors=('#f09133', '#d97a1c', '#c0752a'))

    while current_screen == 'entry_screen':
        screen.blit(background, (0, 0))
        play_button.draw(screen)
        quit_button.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


def levels_screen(screen):
    background = pygame.image.load('assets/levels_screen_background.webp')
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    top_bar = TopBar()
    levels_distance = 75
    levels_move = 0

    def set_levels_move(move: int):
        nonlocal levels_move
        if levels_move == 0:
            levels_move = move

    right_img = pygame.image.load('assets/arrow.png')
    left_img = pygame.transform.rotate(pygame.image.load('assets/arrow.png'), 180)
    right = Button(image=right_img, on_action=lambda: set_levels_move(levels_distance), pos=(WINDOW_WIDTH - 100, 350),
                   width=50, height=50)
    left = Button(image=left_img, on_action=lambda: set_levels_move(-levels_distance), pos=(50, 350), width=50,
                  height=50)
    button_level_width = 50
    current_level = 3
    levels = [1, 2, 3, 4]
    levels_buttons = [Button(text=str(level), width=button_level_width, height=50,
                             pos=(
                                 (level - current_level) * levels_distance + WINDOW_WIDTH / 2 - button_level_width,
                                 450))
                      for level in levels]

    while True:
        screen.blit(background, (0, 0))
        top_bar.draw(screen)
        left.draw(screen)
        right.draw(screen)
        for button in levels_buttons:
            if levels_move != 0:
                if levels_move > 0:
                    button.move(1, 0)
                    levels_move -= 1
                else:
                    button.move(-1, 0)
                    levels_move += 1
            button.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


def game_screen():
    pass


def set_screen(screen: str):
    global current_screen
    current_screen = screen


def run_candy_crush():
    pygame.init()
    pygame.display.set_caption("Candy crush")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    while True:
        if current_screen == "entry_screen":
            entry_screen(screen)
        elif current_screen == "levels_screen":
            levels_screen(screen)
        elif current_screen == "game_screen":
            game_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
