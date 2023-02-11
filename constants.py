WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
FPS = 60

LEVELS_INFO_FILE = 'levels.txt'
USER_INFO_FILE = 'user_info.txt'

# levels screen
INACTIVE_LEVELS_COLORS = ('#cdcccb', '#c6c5c3', '#bebdbb')
PASSED_LEVELS_COLOR = ('#e6ac00', '#d19d00', '#c79500')
CURRENT_LEVEL_COLOR = ('#85b50d', '#82ae13', '#78a112')

# game screen
MAX_LIVES: int = 5

TILE_COLORS = [
    'yellow',
    'green',
    'orange',
    'purple',
    'red',
    'light_blue',
    'dark_blue'
]

# game constants
IMAGE_ID = 'asset_id'
BOARD_COLOR = 'BLACK'
BOARD_TILE_SIZE = 64
EMPTY_SPACE = -1
FALLING_TILE = -2

SPECIAL_TILE = 28

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

SECONDS_PER_LIFE = 600

POSSIBLE_MOVE_PATTERNS = (
    ((0, 1), (1, 0), (2, 0)),
    ((0, 1), (1, 1), (2, 0)),
    ((0, 0), (1, 1), (2, 0)),
    ((0, 1), (1, 0), (2, 1)),
    ((0, 0), (1, 0), (2, 1)),
    ((0, 0), (1, 1), (2, 1)),
    ((0, 0), (0, 2), (0, 3)),
    ((0, 0), (0, 1), (0, 3))
)

DEFAULT_REQUIRED_COLORS = {
    'yellow': 0,
    'green': 0,
    'orange': 0,
    'purple': 0,
    'red': 0,
    'light_blue': 0,
    'dark_blue': 0
}
