from queue import PriorityQueue
from maze.mazes import Maze


def solve(maze: Maze):
    c = 0
    width = maze.width
    total = maze.width*maze.height

    start = maze.start
    end = maze.end

    startpos = start.Position
    endpos = end.Position

    visited = [False]*total
    prev = [None]*total

    inf = float('inf')
    distances = [inf]*total

    completed = False

    distances[start.Position[0]*width+start.Position[1]] = 0
    open_set = PriorityQueue()
    open_set.put((0, c, start))
    open_set_hash = {start}
    count = 0
    while not open_set.empty():
        count += 1
        u = open_set.get()[2]
        open_set_hash.remove(u)
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
                d = abs(vpos[0] - upos[0]) + abs(vpos[1] - upos[1])
                newdistance = distances[uposindex]+d

                if newdistance < distances[vposindex] and visited[vposindex] == False:
                    distances[vposindex] = newdistance
                    prev[vposindex] = u
                    remaining = abs(vpos[0] - endpos[0]) + \
                        abs(vpos[1] - endpos[1])
                    if v not in open_set_hash:
                        c += 1
                        open_set.put((newdistance+remaining, c, v))
                        open_set_hash.add(v)

        visited[uposindex] == True

    from collections import deque
    path = deque()
    current = end
    while (current != None):
        path.appendleft(current)
        current = prev[current.Position[0] * width + current.Position[1]]

    return [path, [count, len(path), completed]]
