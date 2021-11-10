import PathFinding.GUI as p
import tkinter
import tkinter.ttk as ttk
from tkinter import filedialog as fd
from maze import solve as s
from threading import Thread
from time import sleep
from PIL import ImageTk,Image  
import sys

SELECT = 0

def test():
    window = tkinter.Tk()
    window.title("Menu")
    window.resizable(False,False)
    window.minsize(width=400, height=500)
    window.eval('tk::PlaceWindow . center')

    
    notebook = ttk.Notebook(window)

    tab1 = tkinter.Frame(notebook)
    tab2 = tkinter.Frame(notebook)
    
    canvas = tkinter.Canvas(tab1, width = 300, height = 300)  
    canvas.pack()  
    img = Image.open("PathFinding/examples/pf.png")
    rezied = img.resize((300,290), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(rezied)
    canvas.create_image(10, 10, anchor="nw", image=img)

    notebook.add(tab1, text="Path Finding")
    notebook.add(tab2, text="Maze solving")
    notebook.pack()

    labels = []
    def radio_used():
        global SELECT
        SELECT = radio_state.get()
    radio_state = tkinter.IntVar()
    radiobutton1 = tkinter.Radiobutton(tab2,
        text="AStar",font=('segoeuisymbol',14), value=1, variable=radio_state, command=radio_used)
    radiobutton2 = tkinter.Radiobutton(tab2,
        text="Dijkstra",font=('segoeuisymbol',14), value=2, variable=radio_state, command=radio_used)
    radiobutton1.pack()
    radiobutton2.pack()
    
    def addToLabel(str):
        x =tkinter.Label(tab2, text=str,font =("segoeuisymbol",14))
        x.pack()
        labels.append(x)
    
    def btn_add(open_img,type):
        btn_show = tkinter.Button(tab2, text=f"Open img_{type}",font =("segoeuisymbol",14), command=open_img)
        btn_show.pack()
        labels.append(btn_show)

    def solution(filename,type):
        maze, total, img_name, im = s.implement_img(filename)
        addToLabel(f"Node count: {maze.count}")
        addToLabel(f"Time elapsed: {round(total,2)}")
        total, r = s.finding(maze, type)
        addToLabel(f"{type} solving")
        addToLabel(f"Nodes explored: {r[1][0]}")
        if (r[1][2]):
            addToLabel(f"Path found, length: {r[1][1]}")
        else:
            addToLabel("No Path Found")
        addToLabel(f"Creating Maze")
        addToLabel(f"Node count: {maze.count}")
        addToLabel(f"Time elapsed: {round(total,2)}")
        im = s.save_img(im, r, img_name, type)
        def open_img():
            im.show()
        btn_add(open_img,type)

    def threading():
        # Call work function
        t1 = Thread(target=action1)
        t1.start()

    def action():
        window.destroy()
        p.GUI()

    filename = ""

    def action1():
        for label in labels:
            label.destroy()
        filename = fd.askopenfilename()
        if filename == "":return
        addToLabel(f"Loading images")
        addToLabel(f"Creating maze")
        type=""
        if SELECT == 1: type = "astar"
        elif SELECT == 2:type = "dijkstra"
        solution(filename,type)

    button = tkinter.Button(tab1, text="Start Maze on Pygame",font =("segoeuisymbol",14), command=action)
    button.pack()

    button1 = tkinter.Button(tab2, text="Select image",font =("segoeuisymbol",14),
                             command=threading).pack()

    window.update()
    window.mainloop()


# processing
if __name__ == '__main__':
    test()
