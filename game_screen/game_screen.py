import copy
import random
import sys

import pygame
from pygame.constants import MOUSEBUTTONUP, MOUSEBUTTONDOWN

from constants import *


class GameScreen:

    def __init__(self, game):
        self.game = game

        self.font = pygame.font.SysFont("font", 25)
        self.background = pygame.image.load('assets/levels_screen_background.webp')
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.board_height = 9
        self.board_width = 8
        self.margin_vertical = (WINDOW_HEIGHT - self.board_height * BOARD_TILE_SIZE) // 2
        self.margin_horizontal = (WINDOW_WIDTH - self.board_width * BOARD_TILE_SIZE) // 2
        self.board_rectangles = []
        self.create_board_rectangles()

        self.board = None
        self.score: int = 0
        self.moves: int = 0
        self.assets = []
        self.load_assets()

    def create_board_rectangles(self):
        for y in range(self.board_height):
            rects = []
            for x in range(self.board_width):
                rects.append(
                    pygame.Rect((self.margin_horizontal + (x * BOARD_TILE_SIZE),
                                 self.margin_vertical + (y * BOARD_TILE_SIZE),
                                 BOARD_TILE_SIZE,
                                 BOARD_TILE_SIZE))
                )
            self.board_rectangles.append(rects)

    def start_game(self, moves: int = 0, required_gems=[]):
        screen = self.game.screen
        self.moves = moves
        self.score = 0
        self.create_blank_board()
        self.fill_board_and_animate()
        last_mouse_pos = None
        first_selected_tile_pos = None
        while self.moves != 0:
            clicked_space = None
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    if event.pos == last_mouse_pos:
                        clicked_space = self.check_for_tile_click(event.pos)
                    else:
                        first_selected_tile_pos = self.check_for_tile_click(last_mouse_pos)
                        clicked_space = self.check_for_tile_click(event.pos)
                        if not first_selected_tile_pos or not clicked_space:
                            first_selected_tile_pos = None
                            clicked_space = None
                if event.type == MOUSEBUTTONDOWN:
                    last_mouse_pos = event.pos
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if clicked_space:
                if not first_selected_tile_pos:
                    first_selected_tile_pos = clicked_space
                else:
                    first_swapping_tile, second_swapping_tile = \
                        self.get_tiles_to_swap(first_selected_tile_pos, clicked_space)
                    if first_swapping_tile is None and second_swapping_tile is None:
                        first_selected_tile_pos = None  # deselect the first gem
                        continue

                    board_copy = self.copy_board_without_moving_tiles((first_swapping_tile, second_swapping_tile))
                    self.animate_moving_tiles(board_copy, [first_swapping_tile, second_swapping_tile])

                    # Swap the gems in the board data structure.
                    self.board[first_swapping_tile['x']][first_swapping_tile['y']] = second_swapping_tile[IMAGE_ID]
                    self.board[second_swapping_tile['x']][second_swapping_tile['y']] = first_swapping_tile[IMAGE_ID]

                    matched_tiles = self.get_matching_tiles()
                    if not matched_tiles:
                        self.animate_moving_tiles(board_copy, [first_swapping_tile, second_swapping_tile])
                        self.board[first_swapping_tile['x']][first_swapping_tile['y']] = first_swapping_tile[
                            IMAGE_ID]
                        self.board[second_swapping_tile['x']][second_swapping_tile['y']] = second_swapping_tile[
                            IMAGE_ID]
                    else:
                        self.moves -= 1
                        while matched_tiles:
                            for tile_set in matched_tiles:
                                self.score += (10 + (len(tile_set) - 3) * 10)
                                for tile in tile_set:
                                    self.board[tile[0]][tile[1]] = EMPTY_SPACE
                            self.fill_board_and_animate()
                            matched_tiles = self.get_matching_tiles()

                    first_selected_tile_pos = None

            if not self.can_make_move():
                self.create_blank_board()
                self.fill_board_and_animate()

            screen.blit(self.background, (0, 0))
            self.draw_remaining_moves_and_score()
            self.draw_board(self.board)
            pygame.display.update()
            self.game.fps_clock.tick(FPS)

        self.game.set_screen('levels_screen')

    def can_make_move(self):
        for x in range(self.board_height):
            for y in range(self.board_width):
                for pattern in POSSIBLE_MOVE_PATTERNS:
                    if (self.tile_at(self.board, x + pattern[0][0], y + pattern[0][1]) ==
                        self.tile_at(self.board, x + pattern[1][0], y + pattern[1][1]) ==
                        self.tile_at(self.board, x + pattern[2][0], y + pattern[2][1]) is not None) or \
                            (self.tile_at(self.board, x + pattern[0][1], y + pattern[0][0]) ==
                             self.tile_at(self.board, x + pattern[1][1], y + pattern[1][0]) ==
                             self.tile_at(self.board, x + pattern[2][1], y + pattern[2][0]) is not None):
                        return True
        return False

    def check_for_tile_click(self, pos: (int, int)):
        for x in range(self.board_height):
            for y in range(self.board_width):
                if pos is not None and self.board_rectangles[x][y].collidepoint(pos[0], pos[1]):
                    return {'x': x, 'y': y}
        return None

    def get_tiles_to_swap(self, first_tile_pos, second_tile_pos):
        first_tile = {IMAGE_ID: self.board[first_tile_pos['x']][first_tile_pos['y']],
                      'x': first_tile_pos['x'],
                      'y': first_tile_pos['y']}
        second_tile = {IMAGE_ID: self.board[second_tile_pos['x']][second_tile_pos['y']],
                       'x': second_tile_pos['x'],
                       'y': second_tile_pos['y']}
        if first_tile['x'] == second_tile['x'] + 1 and first_tile['y'] == second_tile['y']:
            first_tile['direction'] = UP
            second_tile['direction'] = DOWN
        elif first_tile['x'] == second_tile['x'] - 1 and first_tile['y'] == second_tile['y']:
            first_tile['direction'] = DOWN
            second_tile['direction'] = UP
        elif first_tile['y'] == second_tile['y'] + 1 and first_tile['x'] == second_tile['x']:
            first_tile['direction'] = LEFT
            second_tile['direction'] = RIGHT
        elif first_tile['y'] == second_tile['y'] - 1 and first_tile['x'] == second_tile['x']:
            first_tile['direction'] = RIGHT
            second_tile['direction'] = LEFT
        else:
            return None, None
        return first_tile, second_tile

    def tile_at(self, board, x, y):
        if x < 0 or y < 0 or x >= self.board_height or y >= self.board_width:
            return None
        else:
            return board[x][y]

    def create_blank_board(self):
        self.board = []
        for x in range(self.board_height):
            self.board.append([EMPTY_SPACE] * self.board_width)

    def draw_board(self, board):
        screen = self.game.screen
        for x in range(self.board_height):
            for y in range(self.board_width):
                pygame.draw.rect(screen, BOARD_COLOR, self.board_rectangles[x][y], 1)
                tile = board[x][y]
                if tile != EMPTY_SPACE:
                    screen.blit(self.assets[tile], self.board_rectangles[x][y])

    def get_matching_tiles(self):
        tiles_to_remove = []
        board_copy = copy.deepcopy(self.board)
        for x in range(self.board_height):
            for y in range(self.board_width):
                found_tiles = self.get_tiles_to_remove_around(board_copy, x, y)
                if len(found_tiles) != 0:
                    tiles_to_remove.append(found_tiles)

        return tiles_to_remove

    def get_tiles_to_remove_around(self, board_copy, x, y):
        target_tile = board_copy[x][y]
        if target_tile == self.tile_at(board_copy, x, y + 1) == self.tile_at(board_copy, x, y + 2) \
                and target_tile != EMPTY_SPACE:
            tiles_to_remove = [(x, y), (x, y + 1), (x, y + 2)]
            if self.tile_at(board_copy, x, y + 3) == target_tile:
                tiles_to_remove.append((x, y + 3))
                if self.tile_at(board_copy, x, y + 4) == target_tile:
                    tiles_to_remove.append((x, y + 4))
            if len(tiles_to_remove) == 3 or len(tiles_to_remove) == 4:
                longest_tiles = []
                # look for the longest streak of tiles
                for offset in range(len(tiles_to_remove)):
                    tiles = self.get_same_tiles_above_and_below(board_copy, x, y + offset)
                    if len(tiles) > len(longest_tiles):
                        longest_tiles = tiles
                # to do check if it is 4 remove one
                tiles_to_remove.extend(longest_tiles)
            elif len(tiles_to_remove) == 5:
                # look for more tiles only on the middle tile
                tiles_to_remove.extend(self.get_same_tiles_above_and_below(board_copy, x, y + 2))
            for tile in tiles_to_remove:
                board_copy[tile[0]][tile[1]] = EMPTY_SPACE
            return tiles_to_remove
        if target_tile == self.tile_at(board_copy, x + 1, y) == self.tile_at(board_copy, x + 2, y) \
                and target_tile != EMPTY_SPACE:
            tiles_to_remove = [(x, y), (x + 1, y), (x + 2, y)]
            if self.tile_at(board_copy, x + 3, y) == target_tile:
                tiles_to_remove.append((x + 3, y))
                if self.tile_at(board_copy, x + 4, y) == target_tile:
                    tiles_to_remove.append((x + 4, y))
            if len(tiles_to_remove) == 3 or len(tiles_to_remove) == 4:
                longest_tiles = []
                # look for the longest streak of tiles
                for offset in range(len(tiles_to_remove)):
                    tiles = self.get_same_tiles_left_and_right(board_copy, x + offset, y)
                    if len(tiles) > len(longest_tiles):
                        longest_tiles = tiles
                # to do check if it is 4 remove one
                tiles_to_remove.extend(longest_tiles)
            elif len(tiles_to_remove) == 5:
                # look for more tiles only on the middle tile
                tiles_to_remove.extend(self.get_same_tiles_left_and_right(board_copy, x + 2, y))
            for tile in tiles_to_remove:
                board_copy[tile[0]][tile[1]] = EMPTY_SPACE
            return tiles_to_remove
        return []

    def get_same_tiles_above_and_below(self, board, x, y):
        tiles = []
        target_tile = board[x][y]
        if self.tile_at(board, x - 1, y) == self.tile_at(board, x - 2, y) == target_tile:
            tiles.append((x - 1, y))
            tiles.append((x - 2, y))
        if self.tile_at(board, x + 1, y) == self.tile_at(board, x + 2, y) == target_tile:
            tiles.append((x + 1, y))
            tiles.append((x + 2, y))
        return tiles

    def get_same_tiles_left_and_right(self, board, x, y):
        tiles = []
        target_tile = board[x][y]
        if self.tile_at(board, x, y - 1) == self.tile_at(board, x, y - 2) == target_tile:
            tiles.append((x, y - 1))
            tiles.append((x, y - 2))
        if self.tile_at(board, x, y + 1) == self.tile_at(board, x, y + 2) == target_tile:
            tiles.append((x, y + 1))
            tiles.append((x, y + 2))
        return tiles

    def fill_board_and_animate(self):
        columns_fill = self.get_columns_fill()
        while columns_fill != []:
            moving_tiles = self.get_dropping_tiles()
            for y in range(len(columns_fill[0])):
                if columns_fill[0][y] == EMPTY_SPACE:
                    continue
                moving_tiles.append(
                    {IMAGE_ID: columns_fill[0][y], 'x': FALLING_TILE, 'y': y, 'direction': DOWN}
                )

            board_copy = self.copy_board_without_moving_tiles(moving_tiles)
            self.animate_moving_tiles(board_copy, moving_tiles)
            self.move_tiles(moving_tiles)

            del columns_fill[0]

    def get_columns_fill(self):
        # Returns how many tiles are needed to fill each column in each line
        # and EMPTY_SPACE if none are needed
        board_copy = copy.deepcopy(self.board)
        self.pull_down_tiles(board_copy)

        column_fill = [[] for _ in range(self.board_height)]

        for y in range(self.board_width):
            for x in range(self.board_height):
                if board_copy[x][y] == EMPTY_SPACE:
                    new_tile = random.randint(0, len(self.assets) - 1)
                    board_copy[x][y] = new_tile
                    column_fill[x].append(new_tile)
                else:
                    column_fill[x].append(EMPTY_SPACE)
        return column_fill

    def pull_down_tiles(self, board_copy):
        # pulls all tiles to the bottom if there are any empty spaces
        for y in range(self.board_width):
            tiles_in_column = []
            for x in range(self.board_height):
                if board_copy[x][y] != EMPTY_SPACE:
                    tiles_in_column.append(board_copy[x][y])
            tiles_in_column_index = len(tiles_in_column) - 1
            for x in range(self.board_height - 1, -1, -1):
                if tiles_in_column_index >= 0:
                    board_copy[x][y] = tiles_in_column[tiles_in_column_index]
                    tiles_in_column_index -= 1
                else:
                    board_copy[x][y] = EMPTY_SPACE

    def get_dropping_tiles(self) -> list[dict]:
        dropping_tiles = []
        board_copy = copy.deepcopy(self.board)
        for x in range(self.board_height - 2, -1, -1):
            for y in range(self.board_width):
                if board_copy[x + 1][y] == EMPTY_SPACE and board_copy[x][y] != EMPTY_SPACE:
                    dropping_tiles.append({IMAGE_ID: board_copy[x][y], 'x': x, 'y': y, 'direction': DOWN})
                    board_copy[x][y] = EMPTY_SPACE
        return dropping_tiles

    def copy_board_without_moving_tiles(self, moving_tiles):
        board_copy = copy.deepcopy(self.board)
        for moving_tile in moving_tiles:
            if moving_tile['x'] != FALLING_TILE:
                board_copy[moving_tile['x']][moving_tile['y']] = EMPTY_SPACE
        return board_copy

    def animate_moving_tiles(self, board_copy, moving_tiles):
        screen = self.game.screen
        for progress in range(0, 100, 25):
            screen.blit(self.background, (0, 0))
            self.draw_board(board_copy)
            for tile in moving_tiles:
                self.draw_moving_tile(tile, progress)
            self.draw_remaining_moves_and_score()
            pygame.display.update()
            self.game.fps_clock.tick(FPS)

    def draw_moving_tile(self, tile, progress):
        screen = self.game.screen
        progress *= 0.01
        move_x = 0
        move_y = 0

        if tile['direction'] == UP:
            move_x = -int(progress * BOARD_TILE_SIZE)
        elif tile['direction'] == DOWN:
            move_x = int(progress * BOARD_TILE_SIZE)
        elif tile['direction'] == RIGHT:
            move_y = int(progress * BOARD_TILE_SIZE)
        elif tile['direction'] == LEFT:
            move_y = -int(progress * BOARD_TILE_SIZE)

        tile_x_pos = -1 if tile['x'] == FALLING_TILE else tile['x']
        tile_y_pos = tile['y']

        x_pos = self.margin_vertical + (tile_x_pos * BOARD_TILE_SIZE)
        y_pos = self.margin_horizontal + (tile_y_pos * BOARD_TILE_SIZE)
        screen.blit(
            self.assets[tile[IMAGE_ID]],
            pygame.Rect(y_pos + move_y, x_pos + move_x, BOARD_TILE_SIZE, BOARD_TILE_SIZE)
        )

    def move_tiles(self, moving_tiles):
        for tile in moving_tiles:
            if tile['x'] != FALLING_TILE:
                self.board[tile['x']][tile['y']] = EMPTY_SPACE
                if tile['direction'] == LEFT:
                    self.board[tile['x']][tile['y'] - 1] = tile[IMAGE_ID]
                elif tile['direction'] == RIGHT:
                    self.board[tile['x']][tile['y'] + 1] = tile[IMAGE_ID]
                elif tile['direction'] == DOWN:
                    self.board[tile['x'] + 1][tile['y']] = tile[IMAGE_ID]
                elif tile['direction'] == UP:
                    self.board[tile['x'] - 1][tile['y']] = tile[IMAGE_ID]
            else:
                self.board[0][tile['y']] = tile[IMAGE_ID]

    def draw_remaining_moves_and_score(self):
        moves_text = self.font.render(str(self.moves), True, 'White')
        score_text = self.font.render(str(self.score), True, 'White')
        self.game.screen.blit(moves_text, (20, 20))
        self.game.screen.blit(score_text, (WINDOW_WIDTH - 100, 20))

    def load_assets(self):
        for i in range(6):
            image = pygame.image.load(f'assets/folder/asset{i}.png')
            image = pygame.transform.scale(image, (BOARD_TILE_SIZE, BOARD_TILE_SIZE))
            self.assets.append(image)
