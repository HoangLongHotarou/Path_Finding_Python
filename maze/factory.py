class SolveFactory:
    def __init__(self):
        self.Default = "dijstra"
        self.Choices = ["dijkstra", "Astar"]

    def createsolve(self, type):
        if type == "dijkstra":
            import maze.dijkstra
            return ["Dijktra's Algorithm",maze.dijkstra.solve]
        elif type == "astar":
            import maze.astar
            return ["Astar's Algorithm",maze.astar.solve]
