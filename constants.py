WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
FPS = 60

# game constants
IMAGE_ID = 'asset_id'
BOARD_COLOR = 'BLACK'
BOARD_TILE_SIZE = 64
EMPTY_SPACE = -1
FALLING_TILE = -2

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

POSSIBLE_MOVE_PATTERNS = (((0, 1), (1, 0), (2, 0)),
                          ((0, 1), (1, 1), (2, 0)),
                          ((0, 0), (1, 1), (2, 0)),
                          ((0, 1), (1, 0), (2, 1)),
                          ((0, 0), (1, 0), (2, 1)),
                          ((0, 0), (1, 1), (2, 1)),
                          ((0, 0), (0, 2), (0, 3)),
                          ((0, 0), (0, 1), (0, 3)))
