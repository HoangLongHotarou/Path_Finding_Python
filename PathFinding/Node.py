from pydoc import Doc
from PathFinding.Color import*
import pygame

class Node:
    def __init__(self, row, col, width, total_rows) -> None:
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neghbor = []

    def get_pos(self):
        return self.row, self.col

    def reset(self) -> None:
        self.color = WHITE

    def is_reset(self) -> bool:
        return self.color == WHITE

    def make_open(self) -> None:
        self.color = GREEN

    def make_start(self) -> None:
        self.color = ORANGE

    def make_end(self) -> None:
        self.color = TURQUOISE

    def make_barrier(self) -> None:
        self.color = BLACK

    def make_path(self) -> None:
        self.color = PURPLE

    def make_closed(self) -> None:
        self.color = RED

    def is_start(self) -> bool:
        return self.color == ORANGE

    def is_end(self) -> bool:
        return self.color == TURQUOISE

    def is_barrier(self) -> bool:
        return self.color == BLACK

    def is_closed(self) -> bool:
        return self.color == RED

    def is_open(self) -> bool:
        return self.color == GREEN

    def is_path(self) -> bool:
        return self.color == PURPLE

    def draw(self, win) -> None:
        pygame.draw.rect(
            win, self.color, (self.y, self.x, self.width, self.width))

    def update_neighbor(self, grid) -> None:
        self.neighbors = []
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        # UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        # LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): 
            self.neighbors.append(grid[self.row][self.col - 1])

        '''if use diagonal line :D'''
        # # DOWN RIGHT
        # if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][self.col+1].is_barrier():
        #     self.neighbors.append(grid[self.row + 1][self.col+1])

        # # DOWN LEFT
        # if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col-1].is_barrier():
        #     self.neighbors.append(grid[self.row + 1][self.col-1])
        
        # # UP RIGHT
        # if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][self.col+1].is_barrier():
        #     self.neighbors.append(grid[self.row - 1][self.col+1])

        # # UP LEFT
        # if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col-1].is_barrier():
        #     self.neighbors.append(grid[self.row - 1][self.col-1])

    def __lt__(self, other) -> bool:
        return False
