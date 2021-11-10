class Maze:
    class Node:
        def __init__(self, position):
            self.Position = position
            # index:direct (0:up, 1: right, 2: down, 3: left)
            self.Neighbors = [None, None, None, None]

        # overide like in C#: least than
        def __lt__(self, other):
            return True

    # Optimise convert image to data
    def __init__(self, im):
        # convert img to data
        width, height = im.size
        data = list(im.getdata(0))

        self.start = None
        self.end = None

        # Top row buffer
        topnodes = [None]*width

        # count node
        count = 0

        # Start row
        for x in range(1, width-1):
            if data[x] > 0:
                self.start = Maze.Node((0, x))
                topnodes[x] = self.start
                count += 1
                break

        # Middle
        for y in range(1, height-1):
            '''
                Starting create row offset, row above offset and row below offset
            '''
            rowoffset = y*width
            rowaboveoffset = y*width-width
            rowbelowoffset = y*width+width

            # initialize previous, current and next value
            prv = False
            cur = False
            # Suppose y = 1 and with = 10  --> initial data[10+1] > 0
            nxt = data[rowoffset+1] > 0
            leftnode = None

            for x in range(1, width-1):
                # Move pre, current and next awards.
                # this may we read from the image once per pixel,
                # marginal optmisation
                prv = cur
                cur = nxt
                nxt = data[rowoffset+1+x] > 0
                node = None

                if cur == False:
                    # the wall, no action
                    continue

                # connect the left right of node
                if prv == True:
                    if nxt == True:
                        # PATH PATH PATH
                        # Create node only if paths above of below
                        if data[rowaboveoffset+x] > 0 or data[rowbelowoffset+x] > 0:
                            node = Maze.Node((y, x))
                            leftnode.Neighbors[1] = node
                            node.Neighbors[3] = leftnode
                            leftnode = node
                    else:
                        # PATH PATH WALL
                        # Create path and end of corridor
                        node = Maze.Node((y, x))
                        leftnode.Neighbors[1] = node
                        node.Neighbors[3] = leftnode
                        leftnode = None
                else:
                    if nxt == True:
                        # WALL PATH PATH
                        # Create path at start of corridor
                        node = Maze.Node((y, x))
                        leftnode = node
                    else:
                        # WALL PATH WALL
                        # Create node only if in R.I.P end
                        if data[rowaboveoffset+x] == 0 or data[rowbelowoffset+x] == 0:
                            node = Maze.Node((y, x))

                # If node not None, we can assume we can connect N-S top or dow
                if node != None:
                    # Clear above, connect to waiting top node
                    if data[rowaboveoffset+x] > 0:
                        t = topnodes[x]
                        t.Neighbors[2] = node
                        node.Neighbors[0] = t

                    # If clear bellow, put this new node in the top row for the next connection
                    if data[rowbelowoffset+x] > 0:
                        topnodes[x] = node
                    else:
                        topnodes[x] = None
                    count+=1

        # End row
        rowoffset = (height-1)*width
        for x in range(1, width-1):
            if data[rowoffset+x] > 0:
                self.end = Maze.Node((height-1, x))
                t = topnodes[x]
                t.Neighbors[2] = self.end
                self.end.Neighbors[0] = t
                count += 1
                break

        self.count = count
        self.width = width
        self.height = height
