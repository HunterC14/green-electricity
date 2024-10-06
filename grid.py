# grid.py

import pygame
from pygame import Surface, Rect
from typing import List, Tuple, Optional, Type, Set
from settings import *
from components import Wire, Lever, Lightbulb, Component

class Cell:
    def __init__(self, row: int, col: int) -> None:
        self.row: int = row
        self.col: int = col
        self.rect: Rect = Rect(
            col * CELL_SIZE,
            row * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        self.component: Optional[Component] = None  # Placeholder for components

    def draw(self, surface: Surface) -> None:
        # Draw cell border
        pygame.draw.rect(surface, DARK_GRAY, self.rect, 1)
        # Draw component if it exists
        if self.component:
            self.component.draw(surface, self.rect)

    def handle_click(self, mode: str) -> None:
        if mode == BUILD_MODE:
            pass  # Handled in Grid.handle_click
        elif mode == TEST_MODE and isinstance(self.component, Lever):
            self.component.toggle()

class Grid:
    def __init__(self) -> None:
        self.cells: List[List[Cell]] = [
            [Cell(row, col) for col in range(GRID_COLS)] for row in range(GRID_ROWS)
        ]
        self.selected_component: Type[Component] = Wire  # Default selected component
        self.components: List[Type[Component]] = [Wire, Lever, Lightbulb]  # Available components
        self.panel_rects: List[Tuple[Type[Component], Rect]] = self.create_panel()

    def create_panel(self) -> List[Tuple[Type[Component], Rect]]:
        panel_rects: List[Tuple[Type[Component], Rect]] = []
        for idx, comp in enumerate(self.components):
            rect: Rect = Rect(
                idx * CELL_SIZE,
                GRID_ROWS * CELL_SIZE,  # Position below the grid
                CELL_SIZE,
                CELL_SIZE
            )
            panel_rects.append((comp, rect))
        return panel_rects

    def draw(self, surface: Surface) -> None:
        # Draw grid cells
        for row in self.cells:
            for cell in row:
                cell.draw(surface)

        # Draw panel
        for comp, rect in self.panel_rects:
            pygame.draw.rect(surface, DARK_GRAY, rect)
            # Draw a representation of the component
            temp_comp: Component = comp()
            temp_comp.draw(surface, rect)
            if self.selected_component == comp:
                # Highlight the selected component
                pygame.draw.rect(surface, WHITE, rect, 2)
            else:
                pygame.draw.rect(surface, DARK_GRAY, rect, 2)

    def handle_click(self, pos: Tuple[int, int], mode: str) -> None:
        # Check if clicked on panel
        for comp, rect in self.panel_rects:
            if rect.collidepoint(pos):
                self.selected_component = comp
                return

        # Clicked on grid
        for row in self.cells:
            for cell in row:
                if cell.rect.collidepoint(pos):
                    cell.handle_click(mode)
                    if mode == BUILD_MODE:
                        if cell.component is None:
                            cell.component = self.selected_component()
                        else:
                            cell.component = None  # Remove component
                    return

    def update(self) -> None:
        # Reset power states
        for row in self.cells:
            for cell in row:
                if isinstance(cell.component, (Wire, Lightbulb)):
                    cell.component.powered = False

        # Update power from levers
        for row in self.cells:
            for cell in row:
                if isinstance(cell.component, Lever) and cell.component.on:
                    self.propagate_power(cell.row, cell.col)

    def propagate_power(self, row: int, col: int) -> None:
        directions: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        stack: List[Tuple[int, int]] = [(row, col)]
        visited: Set[Tuple[int, int]] = set()

        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))

            if 0 <= r < GRID_ROWS and 0 <= c < GRID_COLS:
                cell: Cell = self.cells[r][c]
                if isinstance(cell.component, (Wire, Lightbulb)) or (r == row and c == col):
                    if isinstance(cell.component, (Wire, Lightbulb)):
                        cell.component.powered = True
                    # Continue propagation
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS and (nr, nc) not in visited:
                            neighbor_cell = self.cells[nr][nc]
                            if isinstance(neighbor_cell.component, (Wire, Lightbulb)):
                                stack.append((nr, nc))
