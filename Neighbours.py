'''Under construction. This should end up with a simulation about
two types of blocks, red and blue, in an area. Each block
wants to have a certain amount of similar neighbours.
Otherwise, they will move into another location.
'''

from collections import Counter
import tkinter as tk

class Block:
    def __init__(self, position, colour, threshold, satisfied):
        self.position = position
        self.colour = colour
        self.threshold = threshold
        self.satisfied = satisfied

    def __str__(self):
        return(f"Pos: {self.position}, Colour: {self.colour}, Thr: {self.threshold}, Sat: {self.satisfied}")


class Board:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y

    def neighbours(self, i, j):
        neighbours = {(i + k, j + l) for k in range(-1, 2)
                                      for l in range(-1, 2)
                                      if 0 <= i + k <= self.size_x - 1
                                      and 0 <= j + l <= self.size_y - 1}
        neighbours.remove((i, j))
        return neighbours


class Populated_board(Board):
    def __init__(self, size_x, size_y, population): # Pop: set of blocks
        super().__init__(size_x, size_y)
        self.population = population

    def populated_cells(self):
        return {block.position for block in self.population}

    def is_populated(self, i, j):
        return (i, j) in self.populated_cells()

    def get_block(self, i, j):
        for block in self.population:
            if block.position == (i, j):
                return block

    def neighbours(self, i, j):
        neighbour_cells = super().neighbours(i, j)
        neighbours = neighbour_cells & self.populated_cells()
        return {self.get_block(i,j) for (i, j) in neighbours}

    def neighbour_types(self, i, j):
        neighbours = self.neighbours(i, j)
        neighbour_colours = [n.colour for n in neighbours]
        return dict(Counter(neighbour_colours))

    def is_satisfied(self, i, j):
        if self.is_populated(i, j):
            block = self.get_block(i, j)
            similar_neighbours = self.neighbour_types(i, j).get(block.colour, 0)
            return similar_neighbours >= block.threshold


class just_jamming_and_by_jamming_I_mean_testing:
    def __init__(self):
        window = tk.Tk()

        self.cell_size = 20
        self.threshold = 2
        self.canvas_size = 400
        self.number_of_cells = int(self.canvas_size / self.cell_size)
        
        self.population = set()

        self.canvas = tk.Canvas(window, width = self.canvas_size, height = self.canvas_size)
        self.canvas.pack()
               
        for i in range(int(self.canvas_size / self.cell_size)):
            self.canvas.create_line((i + 1)*self.cell_size, 0,
                                    (i + 1)*self.cell_size, self.canvas_size)
        for i in range(int(self.canvas_size / self.cell_size)):
            self.canvas.create_line(0, (i + 1)*self.cell_size,
                                    self.canvas_size, (i + 1)*self.cell_size)

        self.canvas.bind("<Button-1>", self.processButton1)
        self.canvas.bind("<Double-Button-1>", self.processDoubleButton1)
        self.canvas.bind("<Button-3>", self.processButton2)

        frame = tk.Frame(window)
        frame.pack()
        button = tk.Button(frame, text = "Click", command = self.satisfied)
        button.pack()

        window.mainloop()

    def print_cell(self, i, j, color):
        self.canvas.create_rectangle(j*self.cell_size, i*self.cell_size,
                                     (j + 1)*self.cell_size, (i + 1)*self.cell_size,
                                     fill = color)

    def processButton1(self, event):
        i, j = int(event.y / self.cell_size), int(event.x / self.cell_size)
        self.print_cell(i, j, "red")
        self.population.add((i, j, "red"))
        self.population.discard((i, j, "blue"))
        
    def processDoubleButton1(self, event):
        i, j = int(event.y / self.cell_size), int(event.x / self.cell_size)
        self.print_cell(i, j, "blue")
        self.population.add((i, j, "blue") )
        self.population.discard((i, j, "red"))

    def processButton2(self, event):
        i, j = int(event.y / self.cell_size), int(event.x / self.cell_size)
        self.print_cell(i, j, "white")
        self.population.discard((i, j, "blue"))
        self.population.discard((i, j, "red"))



################################################
#### Testing
################################################

    def satisfied(self):
        #for item in self.population:
        #    print(item)
        print("NEWNEWNEWNEWNEWNEWNEWNEWNEWNEWNEWNEWNEWNEWNEWNEWNEWNEW")
        print("****************")
        #### Form the block population assuming that each block is not satisfied
        #### Change this after checking the satisfied-status
        block_population = {Block((i, j), c, self.threshold, False)
                            for i, j, c in self.population}
        for item in block_population:
            print(item)
        print("**************** populated_cells")
        self.populated_board = Populated_board(20, 20, block_population)
        print(self.populated_board.populated_cells())
        print("**************** neighbours (pick one)")
        for block in self.populated_board.neighbours(4,4):
            print(block)
        print("**************** neighbour_types (pick one)")
        print(self.populated_board.neighbour_types(4,4))
        print("**************** satisfied")
        for i, j in self.populated_board.populated_cells():
            print((i, j), ': ', self.populated_board.is_satisfied(i, j), end = "    ")


just_jamming_and_by_jamming_I_mean_testing()
