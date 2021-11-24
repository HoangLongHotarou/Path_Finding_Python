from queue import PriorityQueue
from maze.mazes import Maze
import math


def heuristic(vpos,upos):
    return abs(vpos[0] - upos[0]) + abs(vpos[1] - upos[1])
    # return int(math.sqrt((vpos[0] - upos[0])**2 + (vpos[1] - upos[1])**2))

def solve(maze: Maze):
    count = 0
    width = maze.width
    total = maze.width*maze.height

    start = maze.start
    end = maze.end

    startpos = start.Position
    endpos = end.Position

    # visited = [False]*total
    prev = [None]*total

    inf = float('inf')
    distances = [inf]*total

    completed = False

    distances[start.Position[0]*width+start.Position[1]] = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    explored = 0
    while not open_set.empty():
        explored += 1
        u = open_set.get()[2]
        upos = u.Position
        uposindex = upos[0]*width+upos[1]

        if distances[uposindex] == inf:
            break

        if upos == endpos:
            completed = True
            break

        for v in u.Neighbors:
            if v != None:
                vpos = v.Position
                vposindex = vpos[0]*width+vpos[1]
                d = heuristic(upos,vpos)
                newdistance = distances[uposindex]+d

                # and visited[vposindex] == False
                if newdistance < distances[vposindex]:
                    distances[vposindex] = newdistance
                    prev[vposindex] = u
                    remaining = heuristic(upos,vpos)
                    if v not in open_set.queue:
                        count += 1
                        open_set.put((newdistance+remaining, count, v))

        # visited[uposindex] == True

    from collections import deque
    path = deque()
    current = end
    while (current != None):
        path.appendleft(current)
        current = prev[current.Position[0] * width + current.Position[1]]

    return [path, [explored, len(path), completed]]
