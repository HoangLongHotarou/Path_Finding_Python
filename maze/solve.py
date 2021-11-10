from PIL import Image
import time
from maze.mazes import Maze
from maze.factory import SolveFactory
from threading import *
import time

Image.MAX_IMAGE_PIXELS = None


def convert_image_to_txt(im, img_name):
    w, h = im.size
    print(im.size)
    data = list(im.getdata(0))  # get data R in (R,G,B)
    image_str = [data[index:(index+w)] for index in range(0, len(data), w)]
    with open(f"maze/data/{img_name}.txt", 'w', encoding="utf-8") as f:
        for img in image_str:
            print(img)
            for m in img:
                f.write(str(m)+" ")
            f.write("\n")


def implement_img(src):
    str = src.split('/')

    img_name = str[len(str)-1].split('.')[0]
    # print("Loading Image")
    im = Image.open(f"maze/examples/{img_name}.png")
    # convert_image_to_txt(im,img_name)

    # Create a maze
    print("Creating Maze")
    t0 = time.time()
    maze = Maze(im)
    t1 = time.time()
    # print(f"Node count: {maze.count}")
    total = t1-t0
    # print(f"Time elapsed: {total}\n")
    return maze,total,img_name,im


def finding(maze,type):
    factory = SolveFactory()
    [title, solver] = factory.createsolve(type)
    # [title, solver] = factory.createsolve("dijkstra")
    # print("Starting Solve:", title)
    t0 = time.time()
    [result, starts] = solver(maze)
    t1 = time.time()
    total = t1-t0
    # Print solve starts
    # print("Nodes explored: ", starts[0])
    # if (starts[2]):
    #     print("Path found, length", starts[1])
    # else:
    #     print("No Path Found")
    # print("Time elapsed: ", total, "\n")

    return total, [result, starts]


def save_img(im,solution,img_name, title):
    result, starts = solution

    # print("Saving Image")
    im = im.convert('RGB')
    impixels = im.load()

    resultpath = [n.Position for n in result]

    length = len(resultpath)

    for i in range(0, length - 1):
        a = resultpath[i]
        b = resultpath[i+1]

        # Blue - red
        r = int((i / length) * 255)
        px = (r, 0, 255 - r)

        if a[0] == b[0]:
            # Ys equal - horizontal line
            for x in range(min(a[1], b[1]), max(a[1], b[1])):
                impixels[x, a[0]] = px
        elif a[1] == b[1]:
            # Xs equal - vertical line
            for y in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
                impixels[a[1], y] = px

    im.save(f"maze/solution/{img_name}_{title}.png")
    im.show()
    return im
