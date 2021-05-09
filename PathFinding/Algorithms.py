import tkinter
from queue import PriorityQueue

def tkinter_process2(size):
    window = tkinter.Tk()
    window.title("Announce")
    window.minsize(width=200, height=100)
    label = tkinter.Label(text=f"Size path: {size}")
    label.pack()
    def action():
        window.destroy()
    button = tkinter.Button(text="Exit", command=action)
    button.pack()
    window.update() 
    window.mainloop()


def heuristic(p1, p2)->int:
    x1, y1 = p1
    x2, y2 = p2
    #Euclid distance
    # return int(math.sqrt((x1-x2)**2+(y1-y2)**2))
    # Manhattan distance  --> best match
    return abs(x1-x2)+abs(y1-y2)

def reconstruct_path(came_from,current,draw):
    size = 0
    while current in came_from:
        current = came_from[current]
        current.make_path()
        size+=1
        draw()
    tkinter_process2(size)

def AStar(draw, grid,start,end,count)->bool:
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count,start))
    came_from = {}
    g_score  = {node:float('inf') for row in grid for node in row}
    g_score[start] = 0
    f_score = {node:float('inf') for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(),end.get_pos())
    open_set_hash = {start}
    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            reconstruct_path(came_from,end,draw)
            end.make_end()
            start.make_start()
            draw()
            return True
        for neighbor in current.neighbors:
            temp_g_score = g_score[current]+1
            if temp_g_score<g_score[neighbor]:
                came_from[neighbor]=current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(),end.get_pos())
                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start:
            current.make_closed()
    return False

def Dijkstra(draw, grid,start,end,count)->bool:
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count,start))
    came_from = {}
    g_score  = {node:float('inf') for row in grid for node in row}
    g_score[start] = 0
    # f_score = {node:float('inf') for row in grid for node in row}
    # f_score[start] = heuristic(start.get_pos(),end.get_pos())
    open_set_hash = {start}
    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            reconstruct_path(came_from,end,draw)
            end.make_end()
            start.make_start()
            # x = len(came_from)
            return True
        for neighbor in current.neighbors:
            temp_g_score = g_score[current]+1
            if temp_g_score<g_score[neighbor]:
                came_from[neighbor]=current
                g_score[neighbor] = temp_g_score
                # f_score[neighbor] = temp_g_score+ heuristic(neighbor.get_pos(),end.get_pos())
                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((g_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start:
            current.make_closed()
    return False