from queue import PriorityQueue
from maze.mazes import Maze


def heuristic(vpos, upos):
    # using manhatha
    return abs(vpos[0] - upos[0]) + abs(vpos[1] - upos[1])


def solve(maze: Maze):
    explored = 0
    count = 0
    completed = False
    width = maze.width
    total = width*maze.height

    start = maze.start
    end = maze.end

    startpos = start.Position
    endpos = end.Position

    # visited = [False]*total
    prev = [None]*total

    inf = float('inf')
    distance = [inf]*total

    open_set = PriorityQueue()
    
    open_set.put((0, count, start))
    distance[start.Position[0]*width+start.Position[1]] = 0

    while not open_set.empty():
        explored += 1
        u = open_set.get()[2]
        upos = u.Position

        if distance[upos[0]*width+upos[1]] == inf:
            break

        if u == end:
            completed = True
            break

        for v in u.Neighbors:
            if v != None:
                vpos = v.Position
                d = heuristic(upos,vpos)
                newdistance = distance[upos[0]*width+upos[1]]+d
                # and visited[vpos[0]*width+vpos[1]] == False
                if newdistance < distance[vpos[0]*width+vpos[1]]:
                    distance[vpos[0]*width+vpos[1]] = newdistance
                    prev[vpos[0]*width+vpos[1]] = u
                    if v not in open_set.queue:
                        count += 1
                        open_set.put((newdistance, count, v))
        # visited[upos[0]*width+upos[1]] = True

    from collections import deque
    path = deque()
    current = end
    while current != None:
        path.appendleft(current)
        current = prev[current.Position[0]*width+current.Position[1]]

    return [path, [explored, len(path), completed]]
