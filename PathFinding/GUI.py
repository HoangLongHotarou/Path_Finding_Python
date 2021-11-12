import random
import tkinter
import pygame
from PathFinding.Node import *
from PathFinding.Algorithms import *
import tkinter.ttk as ttk
from PIL import Image
import time
import Program as p
import random

pygame.init()

# Global value
SELECT = 0
size = t0 = t1 = count = 0
step = []
checked = []

FONT1 = pygame.font.SysFont('sans', 35)
FONT2 = pygame.font.SysFont('sans', 30)
FONT3 = pygame.font.SysFont('segoeuisymbol', 20)
FONT4 = pygame.font.SysFont('sans', 15)
FONT5 = pygame.font.SysFont('sans', 18)


TEXT_TITLE = FONT1.render('Path Finding Ver2.0', True, BLACK)
TEXT_INSTRUCTIONS = FONT3.render('Instructions:', True, BLACK)
TEXT_USEG = FONT3.render("♔ g: generate the barrier", True, BLACK)
TEXT_USEG_CAPLOCK = FONT3.render(
    "♔ G: use img to generate the maze", True, BLACK)
TEXT_USEESC = FONT3.render(
    "♔ esc: Escape the processing find path", True, BLACK)
TEXT_USEZ = FONT3.render("♔ z: restart (Just clear path color)", True, BLACK)
TEXT_USESPACE = FONT3.render(
    "♔ space: processing find path to end", True, BLACK)
TEXT_USEC = FONT3.render("♔ c: clear all", True, BLACK)
TEXT_USED = FONT3.render("♔ d: create maze using DFS", True, BLACK)
TEXT_INFOR = FONT4.render("@copyright: Hoang Long - 1911164", True, BLACK)
TEXT_BARRIER = FONT5.render("Barrier", True, BLACK)
TEXT_START = FONT5.render("Start", True, BLACK)
TEXT_END = FONT5.render("End", True, BLACK)
TEXT_PATH = FONT5.render("Path", True, BLACK)



def title(win, width):
    win.blit(TEXT_TITLE, (width+100, 60))
    win.blit(TEXT_INSTRUCTIONS, (width+50, 130))
    win.blit(TEXT_USEESC, (width+50, 160))
    win.blit(TEXT_USEZ, (width+50, 190))
    win.blit(TEXT_USESPACE, (width+50, 220))
    win.blit(TEXT_USEC, (width+50, 250))
    win.blit(TEXT_USEG, (width+50, 280))
    win.blit(TEXT_USEG_CAPLOCK, (width+50, 310))
    win.blit(TEXT_USED, (width+50, 340))
    win.blit(TEXT_INFOR, (width+140, width-50))
    width+=20
    pygame.draw.rect(win, BLACK, (width+50, 380, 20, 20))
    win.blit(TEXT_BARRIER, (width+75, 380))
    pygame.draw.rect(win, ORANGE, (width+130, 380, 20, 20))
    win.blit(TEXT_START, (width+155, 380))
    pygame.draw.rect(win, TURQUOISE, (width+210, 380, 20, 20))
    win.blit(TEXT_END, (width+235, 380))
    pygame.draw.rect(win, PURPLE, (width+290, 380, 20, 20))
    win.blit(TEXT_PATH, (width+315, 380))



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
    gap = (width // rows)
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        pygame.draw.line(win, BLACK, (i * gap, 0), (i * gap, width))
    pygame.draw.line(win, BLACK, (rows * gap, 0), (rows * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    title(win, width)
    print_answer(win, width)
    pygame.display.update()


def get_clicked_node(node, rows, width):
    gap = width // rows
    x, y = node
    row = y // gap
    col = x // gap
    return row, col


def generate_map(grid, rows):
    for _ in range(int(rows*rows*0.3)):
        while True:
            x = random.randint(0, rows-1)
            y = random.randint(0, rows-1)
            barrier = grid[x][y]
            if barrier.is_barrier() == False:
                break
        barrier.make_barrier()


def recursiveDFS(pos, grid):
    movesLeft = ['L', 'R', 'U', 'D']
    i, j = pos
    checked.append((i, j))
    while movesLeft:
        xTemp = i
        yTemp = j
        chooseRandMove = random.randint(0, len(movesLeft)-1)
        currMove = movesLeft.pop(chooseRandMove)
        if currMove == 'L':
            xTemp -= 2
        elif currMove == 'R':
            xTemp += 2
        elif currMove == 'U':
            yTemp += 2
        else:
            yTemp -= 2
        if 0 <= xTemp < len(grid) and 0 <= yTemp < len(grid):
            if (xTemp, yTemp) not in checked and grid[xTemp][yTemp].is_barrier():
                for b in range(min(j, yTemp), max(j, yTemp)+1):
                    for a in range(min(i, xTemp), max(i, xTemp)+1):
                        # if a==0 or b==0 or a==len(grid)-1 or b==len(grid)-1:continue
                        grid[b][a].reset()
                recursiveDFS((xTemp, yTemp), grid)


def generate_map_DFS(grid, rows):
    global checked
    checked = []
    for i in range(rows):
        for j in range(rows):
            grid[j][i].make_barrier()
    x = random.randint(1, rows-1)
    y = random.randint(1, rows-1)
    if(x % 2 == 0 and y % 2 == 0 or x % 2 != 0 and y % 2 != 0):
        x -= 1
    pos = (x, y)
    # print(pos)
    recursiveDFS(pos, grid)


def restart(grid, rows):
    for i in range(rows):
        for j in range(rows):
            temp = grid[i][j]
            if temp.is_open() or temp.is_closed() or temp.is_path():
                temp.reset()


def print_answer(win, width):
    aline = 0
    for s in step:
        pygame.font.init()
        TEXT_ALGORITHM = pygame.font.SysFont('segoeuisymbol', 20).render(
            f"{s[2]} Algorithm: Explored: {s[3]}", True, BLACK)
        TEXT_ANSER = pygame.font.SysFont('segoeuisymbol', 20).render(
            f"Size path: {s[0]}, Time elapsed: {round(s[1],2)}", True, BLACK)
        win.blit(TEXT_ALGORITHM, (width+60, width-340+aline))
        win.blit(TEXT_ANSER, (width+60, width-300+aline))
        aline += 80
    pygame.display.update()


def tkinter_process():
    window = tkinter.Tk()
    window.title("Option")
    window.minsize(width=210, height=100)
    window.resizable(False,False)
    
    def radio_used():
        global SELECT
        SELECT = radio_state.get()
    radio_state = tkinter.IntVar()
    radiobutton1 = tkinter.Radiobutton(
        text="AStar",font=('segoeuisymbol',12), value=1, variable=radio_state, command=radio_used)
    radiobutton2 = tkinter.Radiobutton(
        text="Dijkstra",font=('segoeuisymbol',12), value=2, variable=radio_state, command=radio_used)

    radiobutton1.pack()
    radiobutton2.pack()

    def action():
        window.destroy()

    button = tkinter.Button(text="Click Process",font=('segoeuisymbol',12), command=action).pack()
    window.update()
    window.mainloop()


def convert_image():
    global count
    img = ["normal", "small", "tiny"]
    # r = random()
    if count == len(img):
        count = 0
    im = Image.open(
        f"PathFinding/examples/{img[count]}.png")
    count += 1
    w, h = im.size
    # print(im.size)
    data = list(im.getdata(0))  # get data R in (R,G,B)
    image_str = [data[index:(index+w)] for index in range(0, len(data), w)]
    # print(image_str)
    return image_str


def create_maze_from_image(image, grid, rows):
    for i in range(rows):
        for j in range(rows):
            if image[i][j] == 0:
                # print(grid[i][j].row,grid[i][j].col)
                grid[i][j].make_barrier()


def GUI():
    global size, t1, t0, step, SELECT
    width = 779
    width_screen = int(width*1.6)
    win = pygame.display.set_mode((width_screen, width))
    pygame.display.set_caption("Path Finding")
    # ROWS = 49

    # TEST
    img = convert_image()
    ROWS = len(img)

    grid = make_grid(ROWS, width)

    start = None
    end = None
    barrier = None

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_node(pos, ROWS, width)
                # print(f"({row},{col})")
                if 0 <= row < ROWS and 0 <= col < ROWS:
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
                if 0 <= row < ROWS and 0 <= col < ROWS:
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
                    size = 0
                    count = 0
                    t0 = time.time()
                    if SELECT == 1:
                        restart(grid, ROWS)
                        came_from, count = AStar(lambda: draw(win, grid, ROWS, width),
                                                 grid, start, end)
                        name = "A*"
                    elif SELECT == 2:
                        restart(grid, ROWS)
                        came_from, count = Dijkstra(lambda: draw(win, grid, ROWS, width),
                                                    grid, start, end)
                        name = "Dijkstra"
                    if SELECT != 0:
                        t1 = time.time()
                        if came_from != 0:
                            size = reconstruct_path(
                                came_from, end, lambda: draw(win, grid, ROWS, width))
                            end.make_end()
                            start.make_start()
                        if len(step) >= 2:
                            step.pop(0)
                        step.append([size, t1-t0, name, count])
                        SELECT = 0

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_g:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_LSHIFT or mods & pygame.KMOD_CAPS:
                        img = convert_image()
                        ROWS = len(img)
                        draw(win, grid, ROWS, width)
                        grid = make_grid(ROWS, width)
                        create_maze_from_image(img, grid, ROWS)
                    else:
                        generate_map(grid, ROWS)

                if event.key == pygame.K_d:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    generate_map_DFS(grid, ROWS)

                if event.key == pygame.K_z:
                    restart(grid, ROWS)
        pygame.display.flip()
    pygame.quit()
    p.test()
