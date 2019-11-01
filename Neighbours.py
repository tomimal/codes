'''Under construction. This should end up with a simulation about
two types of blocks, red and blue, in an area. Each block
wants to have a certain amount of similar neighbours.
Otherwise, they will move into another location.
'''

from collections import Counter
import tkinter as tk
import random
import time


def dist1(i, j, k, l):
    '''A distance between cells (i, j) and (k, l) on a board.'''
    return abs(i - k) + abs(j - l)


class Block:
    def __init__(self, position, colour, threshold, satisfied):
        self.position = position
        self.colour = colour
        self.threshold = threshold
        self.satisfied = satisfied

    #### For testing
    def __str__(self):
        return(f"Pos: {self.position}, Colour: {self.colour}, Thr: {self.threshold}, Sat: {self.satisfied}")


class Board:
    ''' A simple board of size "rows x columns" and a method to find the neighbours of a given cell.'''
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        
        self.cells = {(i, j) for i in range(self.rows) for j in range(self.columns)}

    def neighbours(self, i, j):
        neighbours = {(i + k, j + l) for k in range(-1, 2) for l in range(-1, 2)
                      if 0 <= i + k <= self.rows - 1
                      and 0 <= j + l <= self.columns - 1}
        neighbours.remove((i, j))
        return neighbours


class Populated_board(Board):
    ''' Population is a set of blocks. Provide methods to check which
        cells of the board are populated and which are empty.
        The neighbourhood method of Board class is overwritten to give
        the actual neighbours (blocks) instead of cells, some of which might be empty.'''

    def __init__(self, rows, columns, population):
        super().__init__(rows, columns)
        self.population = population

    def populated_cells(self):
        return {block.position for block in self.population}

    def is_populated(self, i, j):
        return (i, j) in self.populated_cells()
    
    def empty_cells(self):
        return self.cells - self.populated_cells()

    def get_block(self, i, j):
        for block in self.population:
            if block.position == (i, j):
                return block

    def neighbours(self, i, j):
        neighbours = super().neighbours(i, j) & self.populated_cells()
        return {self.get_block(i,j) for (i, j) in neighbours}


class Satisfied_blocks(Populated_board):
    ''' Provide methods to check which blocks on the board are satisfied.'''

    def neighbour_types(self, i, j):
        neighbour_colours = [n.colour for n in self.neighbours(i, j)]
        return dict(Counter(neighbour_colours))

    def is_satisfied(self, i, j):
        if self.is_populated(i, j):
            block = self.get_block(i, j)
            similar_neighbours = self.neighbour_types(i, j).get(block.colour, 0)
            return similar_neighbours >= block.threshold

    def satisfied_cells(self):
        return {block.position for block in self.population if self.is_satisfied(*block.position)}

    def unsatisfied_cells(self):
        return self.populated_cells() - self.satisfied_cells()


class Moving_blocks(Satisfied_blocks):
    ''' Find the closest unpopulated cells for a given cell.
        Define methods to move a block to a (randomly chosen) closest empty cell
        and to move all the unsatisfied blocks on the board.'''

    def closest_empty_cells(self, i, j):
        min_dist = min({dist1(i, j, k, l) for k, l in self.empty_cells()})
        return {(k,l) for k, l in self.empty_cells() if dist1(i, j, k, l) == min_dist}
    
    def move(self, i, j):
        block = self.get_block(i, j)
        new_cell = random.choice(tuple(self.closest_empty_cells(i, j)))
        block.position = new_cell

    def move_unsatisfied(self):
        for i, j in self.unsatisfied_cells():
            self.move(i, j)


class just_jamming_and_by_jamming_I_mean_testing:
    def __init__(self):
        window = tk.Tk()

        self.cell_size = 40
        self.canvas_size = 400
        self.number_of_cells = int(self.canvas_size / self.cell_size)

        #### Each block needs two identical neighbours to be satisfied
        self.threshold = 2
        
        self.population = set()
        self.board = Moving_blocks(self.number_of_cells,
                                   self.number_of_cells, self.population)

        self.canvas = tk.Canvas(window, width = self.canvas_size, height = self.canvas_size, bg = "white")
        self.canvas.pack()
               
        for i in range(int(self.canvas_size / self.cell_size)):
            self.canvas.create_line((i + 1)*self.cell_size, 0,
                                    (i + 1)*self.cell_size, self.canvas_size)
        for i in range(int(self.canvas_size / self.cell_size)):
            self.canvas.create_line(0, (i + 1)*self.cell_size,
                                    self.canvas_size, (i + 1)*self.cell_size)

        self.canvas.bind("<Button-1>", self.processButton1)
        self.canvas.bind("<Double-Button-1>", self.processDoubleButton1)
        self.canvas.bind("<Button-3>", self.processButton3)

        frame = tk.Frame(window)
        frame.pack()
        ### Unfinished
        button = tk.Button(frame, text = "Animate", command = self.animate).grid(row = 1, column = 1)
        ### Generate a random population on the board
        button = tk.Button(frame, text = "Random", command = self.random_board).grid(row = 1, column = 2)
        ### Usatisfied blocks are marked with X
        button = tk.Button(frame, text = "Unhappy", command = self.unhappy).grid(row = 1, column = 3)
        ### Move the unsatisfied blocks to another location
        button = tk.Button(frame, text = "Move unhappy", command = self.move_unhappy).grid(row = 1, column = 4)
        
        window.mainloop()

    def print_cell(self, i, j, color):
        self.canvas.create_rectangle(j*self.cell_size, i*self.cell_size,
                                     (j + 1)*self.cell_size, (i + 1)*self.cell_size,
                                     fill = color)

    def print_board(self, board):
        for i, j in board.cells:
            if (i, j) in board.populated_cells():
                self.print_cell(i, j, board.get_block(i, j).colour)
            else:
                self.print_cell(i, j, 'white')

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

    def processButton3(self, event):
        i, j = int(event.y / self.cell_size), int(event.x / self.cell_size)
        self.print_cell(i, j, "white")
        self.population.discard((i, j, "blue"))
        self.population.discard((i, j, "red"))

    def random_board(self):
        for i in range(self.number_of_cells):
            for j in range(self.number_of_cells):
                colour = random.choice(['red', 'blue', 'white'])
                if colour != 'white':
                    self.population.add(Block((i, j), colour, self.threshold, False))
                    self.print_cell(i, j, colour)

    def unhappy(self):
        for (i, j) in self.board.unsatisfied_cells():
            self.canvas.create_text(self.cell_size * (j + 0.5),
                                    self.cell_size * (i + 0.5),
                                    text = "X",
                                    font = "Times 24")

    def move_unhappy(self):
        self.board.move_unsatisfied()
        self.print_board(self.board)

    def animate(self):
        pass


just_jamming_and_by_jamming_I_mean_testing()

