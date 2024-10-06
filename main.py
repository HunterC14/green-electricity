# main.py

import pygame
from pygame import Surface, Rect, font
from typing import Tuple
from settings import *
from grid import Grid

def main() -> None:
    pygame.init()
    screen: Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Green Electricity')
    clock: pygame.time.Clock = pygame.time.Clock()
    pygame.font.init()
    font_obj: font.Font = pygame.font.SysFont(None, BUTTON_FONT_SIZE)

    # Initialize grid
    grid: Grid = Grid()

    # Game state
    mode: str = BUILD_MODE
    running: bool = True

    # Mode button
    button_rect: Rect = Rect(
        SCREEN_WIDTH - BUTTON_WIDTH - 10,  # 10 pixels from the right edge
        GRID_ROWS * CELL_SIZE + (CELL_SIZE - BUTTON_HEIGHT) // 2,  # Vertically centered in the panel
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )

    while running:
        clock.tick(60)  # Limit to 60 FPS

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle mouse clicks and mode switching
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos: Tuple[int, int] = pygame.mouse.get_pos()
                # Check if the mode button was clicked
                if button_rect.collidepoint(pos):
                    # Switch modes when button is clicked
                    mode = TEST_MODE if mode == BUILD_MODE else BUILD_MODE
                else:
                    grid.handle_click(pos, mode)

        # Update logic
        if mode == TEST_MODE:
            grid.update()

        # Drawing
        screen.fill(BLACK)
        grid.draw(screen)

        # Draw mode button
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
        button_text: str = 'TEST MODE' if mode == BUILD_MODE else 'BUILD MODE'
        text_surface = font_obj.render(button_text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

        # Display current mode at the top
        mode_text_surface = font_obj.render(f'Current Mode: {mode}', True, WHITE)
        mode_text_rect = mode_text_surface.get_rect(
            center=(SCREEN_WIDTH // 2, BUTTON_HEIGHT // 2)
        )
        screen.blit(mode_text_surface, mode_text_rect)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
