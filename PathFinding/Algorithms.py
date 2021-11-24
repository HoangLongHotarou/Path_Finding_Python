import tkinter
from queue import PriorityQueue
import pygame
import math
import PathFinding.GUI as GUI
from collections import deque

pygame.init()


def pygame_processing():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.display.quit()
                pygame.quit()
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
    path = deque()
    while current in came_from:
        current = came_from[current]
        path.appendleft(current)
    for i in path:
        pygame_processing()
        i.make_path()
        clock.tick(150)
        draw()


def AStar(draw, grid, start, end):
    clock = pygame.time.Clock()

    count = 0
    explored = 0
    open_set = PriorityQueue()

    start.g_score = 0
    start.f_score = heuristic(start.get_pos(), end.get_pos())
    came_from = {}

    open_set.put(start)
    while not open_set.empty():
        pygame_processing()
        explored += 1
        current = open_set.get()
        if current == end:
            return came_from, explored
        for neighbor in current.neighbors:
            temp_g_score = current.g_score+1
            if temp_g_score < neighbor.g_score:
                came_from[neighbor] = current
                neighbor.g_score = temp_g_score
                neighbor.f_score = temp_g_score + \
                    heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set.queue:
                    count += 1
                    neighbor.count = count
                    open_set.put(neighbor)
                    neighbor.make_open()
        if current != start:
            current.make_closed()
        clock.tick(60)
        draw()
    return 0, explored


def Dijkstra(draw, grid, start, end):
    clock = pygame.time.Clock()
    
    count = 0
    explored = 0
    open_set = PriorityQueue()

    start.g_score = 0
    came_from = {}

    open_set.put(start)
    while not open_set.empty():
        pygame_processing()
        explored += 1
        current = open_set.get()
        if current == end:
            return came_from, explored
        for neighbor in current.neighbors:
            temp_g_score = current.g_score+1
            if temp_g_score < neighbor.g_score:
                came_from[neighbor] = current
                neighbor.g_score = temp_g_score
                if neighbor not in open_set.queue:
                    count += 1
                    neighbor.count = count
                    open_set.put(neighbor)
                    neighbor.make_open()
        if current != start:
            current.make_closed()
        clock.tick(60)
        draw()
    return 0, explored
