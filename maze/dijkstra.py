from queue import PriorityQueue
from maze.mazes import Maze


def solve(maze: Maze):
    count = 0
    c = 0
    completed = False
    width = maze.width
    total = width*maze.height

    start = maze.start
    end = maze.end

    startpos = start.Position
    endpos = end.Position

    visited = [False]*total
    prev = [None]*total

    inf = float('inf')
    distance = [inf]*total

    open_set = PriorityQueue()
    distance[start.Position[0]*width+start.Position[1]]
    open_set.put((0, c, start))
    open_set_hash = {start}
    distance[start.Position[0]*width+start.Position[1]] = 0

    while not open_set.empty():
        count += 1
        u = open_set.get()[2]
        open_set_hash.remove(u)
        upos = u.Position

        if distance[upos[0]*width+upos[1]] == inf:
            break

        if u == end:
            completed = True
            break

        for v in u.Neighbors:
            if v != None:
                vpos = v.Position
                # using manhatha
                d = abs(upos[0]-vpos[0])+abs(upos[1]-vpos[1])
                newdistance = distance[upos[0]*width+upos[1]]+d
                if newdistance < distance[vpos[0]*width+vpos[1]] and visited[vpos[0]*width+vpos[1]] == False:
                    distance[vpos[0]*width+vpos[1]] = newdistance
                    prev[vpos[0]*width+vpos[1]] = u
                    if v not in open_set_hash:
                        c += 1
                        open_set_hash.add(v)
                        open_set.put((newdistance, c, v))
        visited[upos[0]*width+upos[1]] = True

    from collections import deque
    path = deque()
    current = end
    while current != None:
        path.appendleft(current)
        current = prev[current.Position[0]*width+current.Position[1]]

    return [path, [count, len(path), completed]]
