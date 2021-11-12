import tkinter
from queue import PriorityQueue
import pygame
import math
import PathFinding.GUI as GUI
pygame.init()


def pygame_processing():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.display.quit()
                pygame.quit()
                # quit()
                GUI.GUI()
                quit()


def heuristic(p1, p2) -> int:
    x1, y1 = p1
    x2, y2 = p2
    # Euclid distance
    # return int(math.sqrt((x1-x2)**2+(y1-y2)**2))
    # Manhattan distance  --> best match
    return abs(x1-x2)+abs(y1-y2)


def reconstruct_path(came_from, current, draw):
    size = 0
    clock = pygame.time.Clock()
    from collections import deque
    path = deque()
    while current in came_from:
        current = came_from[current]
        path.appendleft(current)

    for i in path:
        pygame_processing()
        i.make_path()
        size += 1
        clock.tick(60)
        draw()
    return size


def AStar(draw, grid, start, end):
    c = 0
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, c, start))
    came_from = {}
    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float('inf') for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())
    visited = {node: False for row in grid for node in row}
    open_set_hash = {start}
    clock = pygame.time.Clock()
    while not open_set.empty():
        pygame_processing()
        count += 1
        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            return came_from, count
        for neighbor in current.neighbors:
            temp_g_score = g_score[current]+1
            if temp_g_score < g_score[neighbor] and visited[neighbor] == False:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + \
                    heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    c += 1
                    open_set.put((f_score[neighbor], c, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        visited[current] = True
        if current != start:
            current.make_closed()
        clock.tick(60)
        draw()
    return 0, count


def Dijkstra(draw, grid, start, end):
    count = 0
    c = 0
    open_set = PriorityQueue()
    open_set.put((0, c, start))
    came_from = {}
    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0
    visited = {node: False for row in grid for node in row}
    open_set_hash = {start}
    clock = pygame.time.Clock()
    while not open_set.empty():
        pygame_processing()
        count += 1
        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            return came_from, count
        for neighbor in current.neighbors:
            temp_g_score = g_score[current]+1
            if temp_g_score < g_score[neighbor] and visited[neighbor] == False:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in open_set_hash:
                    c += 1
                    open_set.put((g_score[neighbor], c, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        visited[current] = True
        if current != start:
            current.make_closed()
        clock.tick(60)
        draw()
    return 0, count
