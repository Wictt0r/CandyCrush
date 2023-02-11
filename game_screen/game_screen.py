import copy
import random
import sys

import pygame
from pygame.constants import MOUSEBUTTONUP, MOUSEBUTTONDOWN

from constants import *


def get_special_tile(original_color: int, special_type: str) -> int:
    """
    :param original_color: the int value of the color
    :param special_type: what effect the resulting tile will have
    :return: the int value of the color with the special effect
    """
    if original_color > 8:
        return original_color
    if special_type == 'vertical':
        return len(TILE_COLORS) + original_color * 3
    if special_type == 'horizontal':
        return len(TILE_COLORS) + original_color * 3 + 1
    if special_type == 'bomb':
        return len(TILE_COLORS) + original_color * 3 + 2
    return original_color


def get_tile_color(tile) -> str:
    """
    :param tile: the int value of the tile
    :return: the color of the tile
    """
    if tile == 0 or tile == 7 or tile == 8 or tile == 9:
        return 'yellow'
    if tile == 1 or tile == 10 or tile == 11 or tile == 12:
        return 'green'
    if tile == 2 or tile == 13 or tile == 14 or tile == 15:
        return 'orange'
    if tile == 3 or tile == 16 or tile == 17 or tile == 18:
        return 'purple'
    if tile == 4 or tile == 19 or tile == 20 or tile == 21:
        return 'red'
    if tile == 5 or tile == 22 or tile == 23 or tile == 24:
        return 'light_blue'
    if tile == 6 or tile == 25 or tile == 26 or tile == 27:
        return 'dark_blue'
    return ''


def get_tile_special_effect(tile: int) -> str:
    """
    :param tile: the int value of the tile
    :return: the tile special effect if there is any
    """
    if tile in range(7, 26, 3):
        return 'vertical'
    if tile in range(8, 27, 3):
        return 'horizontal'
    if tile in range(9, 28, 3):
        return 'bomb'
    return ''


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
        self.required_score = -1
        self.required_colors = DEFAULT_REQUIRED_COLORS
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

    def start_game(self, level_info):
        if level_info is None:
            self.moves = 0
            self.required_score = -1
            self.required_colors = DEFAULT_REQUIRED_COLORS
        else:
            self.moves = level_info['moves']
            self.required_score = level_info['required_score']
            self.required_colors = level_info['required_colors']
        screen = self.game.screen
        self.score = 0
        self.create_board_with_tiles()
        last_mouse_pos = None
        first_selected_tile_pos = None
        while self.moves != 0 and not self.is_level_complete(level_info):
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
                        first_selected_tile_pos = None
                        continue

                    board_copy = self.copy_board_without_moving_tiles(
                        (first_swapping_tile, second_swapping_tile))
                    self.animate_moving_tiles(board_copy,
                                              [first_swapping_tile, second_swapping_tile])

                    self.board[first_swapping_tile['x']][first_swapping_tile['y']] = \
                        second_swapping_tile[IMAGE_ID]
                    self.board[second_swapping_tile['x']][second_swapping_tile['y']] = \
                        first_swapping_tile[IMAGE_ID]

                    matched_tiles = self.get_matching_tiles(first_swapping_tile,
                                                            second_swapping_tile)
                    if not matched_tiles:
                        self.animate_moving_tiles(board_copy,
                                                  [first_swapping_tile, second_swapping_tile])
                        self.board[first_swapping_tile['x']][first_swapping_tile['y']] = \
                            first_swapping_tile[
                                IMAGE_ID]
                        self.board[second_swapping_tile['x']][second_swapping_tile['y']] = \
                            second_swapping_tile[
                                IMAGE_ID]
                    else:
                        self.moves -= 1
                        while matched_tiles:
                            for tile_set in matched_tiles:
                                self.score += (10 + (len(tile_set) - 3) * 10)
                                for tile in tile_set:
                                    self.remove_tile_from_required_colors(tile)
                                    self.board[tile[0]][tile[1]] = EMPTY_SPACE
                            self.fill_board_and_animate()
                            matched_tiles = self.get_matching_tiles()

                    first_selected_tile_pos = None

            if not self.can_make_move():
                self.create_board_with_tiles()

            screen.blit(self.background, (0, 0))
            self.draw_stats()
            self.draw_board(self.board)
            pygame.display.update()
            self.game.fps_clock.tick(FPS)
        self.game.set_screen('levels_screen')
        return self.is_level_complete(level_info)

    def can_make_move(self):
        for x in range(self.board_height):
            for y in range(self.board_width):
                for pattern in POSSIBLE_MOVE_PATTERNS:
                    if (self.tile_at(self.board, x + pattern[0][0], y + pattern[0][1]) ==
                        self.tile_at(self.board, x + pattern[1][0], y + pattern[1][1]) ==
                        self.tile_at(self.board, x + pattern[2][0],
                                     y + pattern[2][1]) is not None) or \
                            (self.tile_at(self.board, x + pattern[0][1], y + pattern[0][0]) ==
                             self.tile_at(self.board, x + pattern[1][1], y + pattern[1][0]) ==
                             self.tile_at(self.board, x + pattern[2][1],
                                          y + pattern[2][0]) is not None):
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

    def create_board_with_tiles(self):
        """
        Generates a board with no current matches
        """
        self.create_blank_board()
        self.fill_board_and_animate(animate=False)
        while self.get_matching_tiles() != []:
            self.create_blank_board()
            self.fill_board_and_animate(animate=False)

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

    def get_matching_tiles(self, first_matching_tile=None, second_matching_tile=None):
        tiles_to_remove = []
        board_copy = copy.deepcopy(self.board)
        if first_matching_tile is not None and second_matching_tile is not None:
            found_matches = \
                self.get_special_matches(board_copy, first_matching_tile, second_matching_tile)
            if found_matches != []:
                return [list(set(found_matches))]

        for x in range(self.board_height):
            for y in range(self.board_width):
                found_matches = \
                    self.get_tiles_to_remove_around(board_copy, x, y, first_matching_tile,
                                                    second_matching_tile)
                if len(found_matches) != 0:
                    tiles_to_remove.append(list(set(found_matches)))

        return tiles_to_remove

    def get_special_matches(self, board_copy, first_matching_tile_pos, second_matching_tile_pos):
        tiles_to_remove = []
        first_tile = first_matching_tile_pos[IMAGE_ID]
        second_tile = second_matching_tile_pos[IMAGE_ID]
        first_tile_effect = get_tile_special_effect(first_tile)
        second_tile_effect = get_tile_special_effect(second_tile)
        if first_tile == SPECIAL_TILE and second_tile == SPECIAL_TILE:
            for x_remove in range(self.board_height):
                for y_remove in range(self.board_width):
                    board_copy[x_remove][y_remove] = EMPTY_SPACE
                    tiles_to_remove.append((x_remove, y_remove))
        elif first_tile == SPECIAL_TILE or second_tile == SPECIAL_TILE:
            if first_tile == SPECIAL_TILE:
                tiles_to_remove.extend(
                    self.remove_all_tiles_of_color(board_copy, get_tile_color(second_tile),
                                                   second_tile_effect)
                )
                tiles_to_remove.append(
                    (second_matching_tile_pos['x'], second_matching_tile_pos['y']))
            else:
                tiles_to_remove.extend(
                    self.remove_all_tiles_of_color(board_copy, get_tile_color(first_tile),
                                                   first_tile_effect)
                )
                tiles_to_remove.append(
                    (first_matching_tile_pos['x'], first_matching_tile_pos['y']))

        elif first_tile_effect == second_tile_effect == 'bomb':
            tiles_to_remove = self.apply_bomb(board_copy, second_matching_tile_pos['x'],
                                              second_matching_tile_pos['y'], 2)

        elif (first_tile_effect == 'horizontal' or first_tile_effect == 'vertical') and \
                (second_tile_effect == 'horizontal' or second_tile_effect == 'vertical'):
            tiles_to_remove.extend(
                self.apply_special_effect(board_copy,
                                          x=second_matching_tile_pos['x'],
                                          y=second_matching_tile_pos['y'],
                                          special_effect='vertical')
            )
            tiles_to_remove.extend(
                self.apply_special_effect(board_copy,
                                          x=second_matching_tile_pos['x'],
                                          y=second_matching_tile_pos['y'],
                                          special_effect='horizontal')
            )
        elif ((first_tile_effect == 'horizontal' or first_tile_effect == 'vertical') and
              second_tile_effect == 'bomb') or \
                (first_tile_effect == 'bomb' and (second_tile_effect == 'horizontal' or
                                                  second_tile_effect == 'vertical')):
            if second_matching_tile_pos['y'] - 1 > 0:
                tiles_to_remove.extend(
                    self.apply_special_effect(board_copy,
                                              x=second_matching_tile_pos['x'],
                                              y=second_matching_tile_pos['y'] - 1,
                                              special_effect='vertical')
                )
            tiles_to_remove.extend(
                self.apply_special_effect(board_copy,
                                          x=second_matching_tile_pos['x'],
                                          y=second_matching_tile_pos['y'],
                                          special_effect='vertical')
            )
            if second_matching_tile_pos['y'] + 1 < self.board_width:
                tiles_to_remove.extend(
                    self.apply_special_effect(board_copy,
                                              x=second_matching_tile_pos['x'],
                                              y=second_matching_tile_pos['y'] + 1,
                                              special_effect='vertical')
                )
            if second_matching_tile_pos['x'] - 1 > 0:
                tiles_to_remove.extend(
                    self.apply_special_effect(board_copy,
                                              x=second_matching_tile_pos['x'] - 1,
                                              y=second_matching_tile_pos['y'],
                                              special_effect='horizontal')
                )
            tiles_to_remove.extend(
                self.apply_special_effect(board_copy,
                                          x=second_matching_tile_pos['x'],
                                          y=second_matching_tile_pos['y'],
                                          special_effect='horizontal')
            )
            if second_matching_tile_pos['x'] + 1 < self.board_height:
                tiles_to_remove.extend(
                    self.apply_special_effect(board_copy,
                                              x=second_matching_tile_pos['x'] + 1,
                                              y=second_matching_tile_pos['y'],
                                              special_effect='horizontal')
                )
        return tiles_to_remove

    def remove_all_tiles_of_color(self, board_copy, color, special):
        removed_tiles = []
        for y in range(self.board_width):
            for x in range(self.board_height):
                if get_tile_color(board_copy[x][y]) == color:
                    tile_special_effect = get_tile_special_effect(board_copy[x][y])
                    if tile_special_effect == '' and special != '':
                        tile_special_effect = special
                    if tile_special_effect != '':
                        removed_tiles.extend(
                            self.apply_special_effect(board_copy, tile_special_effect, x, y)
                        )
                    board_copy[x][y] = EMPTY_SPACE
                    removed_tiles.append((x, y))
        return removed_tiles

    def get_tiles_to_remove_around(self, board_copy, x, y, first_matching_tile,
                                   second_matching_tile):
        tiles_to_remove = []
        target_tile = board_copy[x][y]
        if target_tile == SPECIAL_TILE:
            return tiles_to_remove
        target_tile_color = get_tile_color(target_tile)
        if first_matching_tile is not None and second_matching_tile is not None:
            first_switched_tile = (first_matching_tile['x'], first_matching_tile['y'])
            second_switched_tile = (second_matching_tile['x'], second_matching_tile['y'])
        else:
            first_switched_tile = (x, y)
            second_switched_tile = (x, y)
        if target_tile_color == get_tile_color(self.tile_at(board_copy, x, y + 1)) == \
                get_tile_color(self.tile_at(board_copy, x, y + 2)) \
                and target_tile != EMPTY_SPACE:
            tiles_to_remove.extend(
                self.get_tiles_to_remove_direction(board_copy, x, y, first_switched_tile,
                                                   second_switched_tile, 'horizontal')
            )
        elif target_tile_color == get_tile_color(self.tile_at(board_copy, x + 1, y)) == \
                get_tile_color(self.tile_at(board_copy, x + 2, y)) \
                and target_tile != EMPTY_SPACE:
            tiles_to_remove.extend(
                self.get_tiles_to_remove_direction(board_copy, x, y, first_switched_tile,
                                                   second_switched_tile, 'vertical')
            )
        for tile in tiles_to_remove:
            special_effect = get_tile_special_effect(board_copy[tile[0]][tile[1]])
            if special_effect != '':
                tiles_to_remove.extend(
                    self.apply_special_effect(board_copy, special_effect, tile[0], tile[1]))
            board_copy[tile[0]][tile[1]] = EMPTY_SPACE
        return tiles_to_remove

    def get_tiles_to_remove_direction(self, board_copy, x, y, first_switched_tile,
                                      second_switched_tile, direction):
        target_tile = board_copy[x][y]
        target_tile_color = get_tile_color(target_tile)
        if direction == 'horizontal':
            tiles_to_remove = [(x, y), (x, y + 1), (x, y + 2)]
            if get_tile_color(self.tile_at(board_copy, x, y + 3)) == target_tile_color:
                tiles_to_remove.append((x, y + 3))
                if get_tile_color(self.tile_at(board_copy, x, y + 4)) == target_tile_color:
                    tiles_to_remove.append((x, y + 4))
        else:
            tiles_to_remove = [(x, y), (x + 1, y), (x + 2, y)]
            if get_tile_color(self.tile_at(board_copy, x + 3, y)) == target_tile_color:
                tiles_to_remove.append((x + 3, y))
                if get_tile_color(self.tile_at(board_copy, x + 4, y)) == target_tile_color:
                    tiles_to_remove.append((x + 4, y))
        if len(tiles_to_remove) == 3 or len(tiles_to_remove) == 4:
            longest_tiles = []
            longest_tiles_index = 0
            # look for the longest streak of tiles
            for offset in range(len(tiles_to_remove)):
                if direction == 'horizontal':
                    tiles = self.get_same_tiles_above_and_below(board_copy, x, y + offset)
                else:
                    tiles = self.get_same_tiles_left_and_right(board_copy, x + offset, y)
                if len(tiles) > len(longest_tiles):
                    longest_tiles = tiles
                    longest_tiles_index = offset
            # to do check if it is 4 remove one
            if len(longest_tiles) == 0 and len(tiles_to_remove) == 4:
                tile_to_add = get_special_tile(target_tile, direction)
                if first_switched_tile in tiles_to_remove:
                    tiles_to_remove.remove(first_switched_tile)
                    self.board[first_switched_tile[0]][first_switched_tile[1]] = tile_to_add
                elif second_switched_tile in tiles_to_remove:
                    tiles_to_remove.remove(second_switched_tile)
                    self.board[second_switched_tile[0]][second_switched_tile[1]] = tile_to_add
            elif len(longest_tiles) == 2 or len(longest_tiles) == 4:
                if direction == 'horizontal':
                    tiles_to_remove.remove((x, y + longest_tiles_index))
                    special_tile_type = 'special' if len(longest_tiles) == 4 else 'bomb'
                    self.board[x][y + longest_tiles_index] = \
                        get_special_tile(target_tile, special_tile_type)
                else:
                    tiles_to_remove.remove((x + longest_tiles_index, y))
                    special_tile_type = 'special' if len(longest_tiles) == 4 else 'bomb'
                    self.board[x + longest_tiles_index][y] = \
                        get_special_tile(target_tile, special_tile_type)
            tiles_to_remove.extend(longest_tiles)
        elif len(tiles_to_remove) >= 5:
            # look for more tiles only on the middle tile
            if direction == 'horizontal':
                tiles_to_remove.extend(self.get_same_tiles_above_and_below(board_copy, x, y + 2))
                tiles_to_remove.remove((x, y + 2))
                self.board[x][y + 2] = SPECIAL_TILE
            else:
                tiles_to_remove.extend(self.get_same_tiles_left_and_right(board_copy, x + 2, y))
                tiles_to_remove.remove((x + 2, y))
                self.board[x + 2][y] = SPECIAL_TILE
        return tiles_to_remove

    def get_same_tiles_above_and_below(self, board, x, y):
        tiles = []
        target_tile = self.tile_at(board, x, y)
        if target_tile is None:
            return tiles
        target_tile_color = get_tile_color(target_tile)
        tile_above = self.tile_at(board, x - 1, y)
        two_tiles_above = self.tile_at(board, x - 2, y)
        tile_below = self.tile_at(board, x + 1, y)
        two_tiles_below = self.tile_at(board, x + 2, y)
        if tile_above is not None and two_tiles_above is not None and \
                get_tile_color(tile_above) == get_tile_color(two_tiles_above) == target_tile_color:
            tiles.append((x - 1, y))
            tiles.append((x - 2, y))
        if tile_below is not None and two_tiles_below is not None and \
                get_tile_color(tile_below) == get_tile_color(two_tiles_below) == target_tile_color:
            tiles.append((x + 1, y))
            tiles.append((x + 2, y))
        if tile_above is not None and tile_below is not None and \
                get_tile_color(tile_above) == get_tile_color(tile_below) == target_tile_color:
            tiles.append((x - 1, y))
            tiles.append((x + 1, y))
        return tiles

    def get_same_tiles_left_and_right(self, board, x, y):
        tiles = []
        target_tile = self.tile_at(board, x, y)
        if target_tile is None:
            return tiles
        target_tile_color = get_tile_color(target_tile)
        tile_left = self.tile_at(board, x, y - 1)
        two_tiles_left = self.tile_at(board, x, y - 2)
        tile_right = self.tile_at(board, x, y + 1)
        two_tiles_right = self.tile_at(board, x, y + 2)
        if tile_left is not None and two_tiles_left is not None and \
                get_tile_color(tile_left) == get_tile_color(two_tiles_left) == target_tile_color:
            tiles.append((x, y - 1))
            tiles.append((x, y - 2))
        if tile_right is not None and two_tiles_right is not None and \
                get_tile_color(tile_right) == get_tile_color(two_tiles_right) == target_tile_color:
            tiles.append((x, y + 1))
            tiles.append((x, y + 2))
        if tile_left is not None and tile_right is not None and \
                get_tile_color(tile_left) == get_tile_color(tile_right) == target_tile_color:
            tiles.append((x, y - 1))
            tiles.append((x, y + 1))
        return tiles

    def fill_board_and_animate(self, animate: bool = True):
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
            if animate:
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
                    new_tile = random.randint(0, len(TILE_COLORS) - 1)
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
                    dropping_tiles.append(
                        {IMAGE_ID: board_copy[x][y], 'x': x, 'y': y, 'direction': DOWN})
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
            self.draw_stats()
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

    def is_level_complete(self, level_info) -> bool:
        if level_info['required_score'] != -1 and self.score < level_info['required_score'] != -1:
            return False
        for color in TILE_COLORS:
            if level_info['required_colors'][color] != 0:
                return False
        return True

    def apply_special_effect(self, board_copy, special_effect, x, y):
        tiles_to_remove = []
        if special_effect == 'horizontal':
            for remove_y in range(self.board_width):
                tile_special_effect = get_tile_special_effect(board_copy[x][remove_y])
                board_copy[x][remove_y] = EMPTY_SPACE
                tiles_to_remove.append((x, remove_y))
                if tile_special_effect != 'horizontal' and tile_special_effect != '' and remove_y != y:
                    tiles_to_remove.extend(
                        self.apply_special_effect(board_copy, tile_special_effect, x, remove_y)
                    )
        elif special_effect == 'vertical':
            for remove_x in range(self.board_height):
                tile_special_effect = get_tile_special_effect(board_copy[remove_x][y])
                board_copy[remove_x][y] = EMPTY_SPACE
                tiles_to_remove.append((remove_x, y))
                if tile_special_effect != 'vertical' and tile_special_effect != '' and remove_x != x:
                    tiles_to_remove.extend(
                        self.apply_special_effect(board_copy, tile_special_effect, remove_x, y)
                    )
        elif special_effect == 'bomb':
            tiles_to_remove.extend(self.apply_bomb(board_copy, x, y, 1))
        return tiles_to_remove

    def apply_bomb(self, board_copy, x, y, bomb_radius):
        tiles_to_remove = []
        for remove_x in (x - bomb_radius, x, x + bomb_radius):
            for remove_y in (y - bomb_radius, y, y + bomb_radius):
                if remove_x < 0 or remove_y < 0 or remove_x >= self.board_height or \
                        remove_y >= self.board_width:
                    continue
                tile_special_effect = get_tile_special_effect(board_copy[remove_x][remove_y])
                board_copy[remove_x][remove_y] = EMPTY_SPACE
                tiles_to_remove.append((remove_x, remove_y))
                if tile_special_effect != '':
                    tiles_to_remove.extend(
                        self.apply_special_effect(board_copy, tile_special_effect, remove_x,
                                                  remove_y)
                    )
        return tiles_to_remove

    def draw_stats(self):
        moves_text = self.font.render('Moves left: ' + str(self.moves), True, 'White')
        score_text = self.font.render('Score: ' + str(self.score), True, 'White')
        self.game.screen.blit(moves_text, (20, 20))
        self.game.screen.blit(score_text, (WINDOW_WIDTH - 150, 20))

    def load_assets(self):
        for i in range(29):
            image = pygame.image.load(f'assets/tiles/asset{i}.png')
            image = pygame.transform.scale(image, (BOARD_TILE_SIZE - 3, BOARD_TILE_SIZE - 3))
            self.assets.append(image)

    def remove_tile_from_required_colors(self, tile_pos):
        tile = self.tile_at(self.board, tile_pos[0], tile_pos[1])
        if tile is None:
            return
        tile_color = get_tile_color(tile)
        if self.required_colors[tile_color] != 0 and self.required_colors[tile_color] != -1:
            self.required_colors[tile_color] -= 1
