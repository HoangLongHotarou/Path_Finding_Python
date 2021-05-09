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
        return self.row,self.col

    def reset(self) -> None:
        self.color = WHITE

    def is_reset(self)->bool:
        return self.color == WHITE
    
    def make_open(self)->None:
        self.color = GREEN

    def make_start(self) -> None:
        self.color = ORANGE

    def make_end(self) -> None:
        self.color = TURQUOISE

    def make_barrier(self) -> None:
        self.color = BLACK

    def make_path(self) -> None:
        self.color = PURPLE

    def make_closed(self)->None:
        self.color = RED

    def is_start(self) -> bool:
        return self.color == ORANGE

    def is_end(self) -> bool:
        return self.color == TURQUOISE

    def is_barrier(self) -> bool:
        return self.color == BLACK

    def is_closed(self) -> bool:
        return self.color == GREEN

    def is_open(self) -> bool:
        return self.color == RED
    
    def is_path(self) -> bool:
        return self.color == PURPLE

    def draw(self, win) -> None:
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbor(self, grid) -> None:
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other)->bool:
        return False
