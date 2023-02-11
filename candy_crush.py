import copy
import os.path
import time
from datetime import datetime

import sys

import pygame

from constants import *
from entry_screen.entry_screen import EntryScreen
from game_screen.game_screen import GameScreen
from levels_screen.levels_screen import LevelsScreen


class CandyCrush:
    def __init__(self):
        pygame.init()
        self.current_screen = "entry_screen"
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.lives = 0
        self.last_life_gain_timestamp = 0
        self.current_max_level = 0
        self.level_to_play = None
        self.levels_info: [dict] = []
        self.load_levels_info()
        self.load_user_info()
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
                game_result = self.game_screen.start_game(
                    level_info=copy.deepcopy(self.levels_info[self.level_to_play])
                )
                if game_result:
                    if self.level_to_play == self.current_max_level:
                        self.current_max_level += 1
                else:
                    self.lives -= 1
                self.save_user_info()
            self.check_for_quit()
            pygame.display.update()
            self.fps_clock.tick(FPS)

    def check_for_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def load_levels_info(self):
        if not os.path.exists(LEVELS_INFO_FILE):
            raise Exception('Can not load levels information. File missing.')
        with open(LEVELS_INFO_FILE) as level_file:
            for level_info in level_file:
                level_info_parts = level_info.split(' ')
                moves = int(level_info_parts[0])
                required_score = int(level_info_parts[1])
                colors = {}
                for color_index in range(len(TILE_COLORS)):
                    colors[TILE_COLORS[color_index]] = int(level_info_parts[color_index + 2])
                self.levels_info.append({
                    'moves': moves,
                    'required_score': required_score,
                    'required_colors': colors
                })

    def increase_lives(self):
        if self.lives < MAX_LIVES:
            self.lives += 1
            self.last_life_gain_timestamp = int(time.time())
            self.save_user_info()

    def load_user_info(self):
        if not os.path.exists(USER_INFO_FILE):
            self.last_life_gain_timestamp = int(time.time())
            self.lives = MAX_LIVES
            self.current_max_level = 0
            return
        with open(USER_INFO_FILE, mode='r') as user_file:
            lives_timestamp = datetime.fromtimestamp(float(user_file.readline()))
            lives_timestamp = int(time.mktime(lives_timestamp.timetuple()))
            self.lives = int(user_file.readline())
            self.current_max_level = int(user_file.readline())
        if self.lives != MAX_LIVES:
            current_time = int(time.time())
            lives_increase = (current_time - lives_timestamp) // SECONDS_PER_LIFE
            if lives_increase + self.lives > MAX_LIVES:
                self.lives = MAX_LIVES
                self.last_life_gain_timestamp = current_time
            else:
                self.lives += lives_increase
                self.last_life_gain_timestamp = lives_timestamp + lives_increase * SECONDS_PER_LIFE
        else:
            self.last_life_gain_timestamp = int(time.time())

    def save_user_info(self):
        with open(USER_INFO_FILE, 'w') as user_file:
            user_file.write(str(self.last_life_gain_timestamp) + '\n')
            user_file.write(str(self.lives) + '\n')
            user_file.write(str(self.current_max_level) + '\n')
