# settings.py

from typing import Tuple

# Screen dimensions
GRID_ROWS: int = 10
GRID_COLS: int = 16
CELL_SIZE: int = 40  # Size of each cell in pixels

SCREEN_WIDTH: int = GRID_COLS * CELL_SIZE
SCREEN_HEIGHT: int = GRID_ROWS * CELL_SIZE + CELL_SIZE  # Extra space for bottom panel

# Button settings
BUTTON_WIDTH: int = 100
BUTTON_HEIGHT: int = 40
BUTTON_COLOR: Tuple[int, int, int] = (50, 50, 50)  # DARK_GRAY
BUTTON_TEXT_COLOR: Tuple[int, int, int] = (255, 255, 255)  # WHITE
BUTTON_FONT_SIZE: int = 20

# Colors (RGB)
Color = Tuple[int, int, int]
BLACK: Color = (0, 0, 0)
DARK_GREEN: Color = (0, 100, 0)
LIGHT_GREEN: Color = (0, 255, 0)
DARK_GRAY: Color = (50, 50, 50)
LIGHT_GRAY: Color = (200, 200, 200)
BROWN: Color = (139, 69, 19)
WHITE: Color = (255, 255, 255)

# Modes
BUILD_MODE: str = 'BUILD'
TEST_MODE: str = 'TEST'
