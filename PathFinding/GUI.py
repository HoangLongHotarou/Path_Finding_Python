import random
import tkinter
from PathFinding.Node import *
from PathFinding.Algorithms import *

WIDTH = 800
WIN = pygame.display.set_mode((800, 800))
ROWS = 50
pygame.display.set_caption("Path Finding")
SELECT = 0

#tkinter


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_node(node, rows, width):
    gap = width // rows
    y, x = node
    row = y // gap
    col = x // gap
    return row, col


def generate_map(grid, rows, barrier):
    for _ in range(int(rows*rows*0.3)):
        while True:
            x = random.randint(0, rows-1)
            y = random.randint(0, rows-1)
            barrier = grid[x][y]
            if barrier.is_barrier() == False:
                break
        barrier.make_barrier()


def restart(grid, rows):
    for i in range(rows):
        for j in range(rows):
            temp = grid[i][j]
            if temp.is_open() or temp.is_closed() or temp.is_path():
                temp.reset()

def tkinter_process():
    window = tkinter.Tk()
    window.title("Option")
    window.minsize(width=200, height=100)

    def radio_used():
        global SELECT
        SELECT = radio_state.get()
    radio_state = tkinter.IntVar()
    radiobutton1 = tkinter.Radiobutton(text="AStar", value=1, variable=radio_state, command=radio_used)
    radiobutton2 = tkinter.Radiobutton(text="Dijkstra", value=2, variable=radio_state, command=radio_used)

    radiobutton1.pack()
    radiobutton2.pack()

    def action():
        window.destroy()
    # calls action() when pressed
    button = tkinter.Button(text="Click Process", command=action)
    button.pack()
    window.update() 
    window.mainloop()


def GUI(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None
    barrier = None
    count = 0

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_node(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    barrier = node
                    barrier.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_node(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbor(grid)
                    tkinter_process()
                    if(SELECT == 1):
                        AStar(lambda: draw(win, grid, ROWS, width), grid, start, end,count)
                    else:
                        Dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end,count)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_g:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    generate_map(grid, ROWS, barrier)

                if event.key == pygame.K_z:
                    restart(grid, ROWS)
    pygame.quit()
