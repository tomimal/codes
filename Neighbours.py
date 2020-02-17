'''Under construction. This should end up with a simulation about
two types of blocks, red and blue, living in an area. Each block
needs to have a certain amount of similar neighbours.
Otherwise, they will move into another location.

FIX: Stop simulation when the board stabilizes. The current value is 20 iterations,
but for small boards this is too much.

The "Unhappy button" is used only for testing.
'''

from Boards import MovingItems
from tkinter import *
import random


class NeighboursSimulation:
    def __init__(self, testing = False):
        self.testing = testing
        root = Tk()

        ########################################################################
        ### Create a canvas to display the population.
        ### Initialize with a random population.
        ### FIXED VALUES...
        ### Make a smaller board if testing.
        ########################################################################
        self.canvasSize = 400
        self.population = {}
        n = 8 if self.testing else 20
        self.cellSize = 400 / n
        for i in range(n):
            for j in range(n):
                self.population[i, j] = random.choice(['red', 'blue', 'white'])
        self.process = MovingItems(n, n, self.population)
        ########################################################################
        ### Requires cleaning...
        ########################################################################


        self.canvas = Canvas(width = self.canvasSize,
                             height = self.canvasSize,
                             bg = "white")
        self.canvas.pack()
        self.printBoard()

        ### User may create red, blue, and white cells on the board using the mouse buttons.
        self.canvas.bind("<Button-1>", self.leftButton)
        self.canvas.bind("<Double-Button-1>", self.leftDoubleButton1)
        self.canvas.bind("<Button-3>", self.rightButton)

        frame = Frame(root)
        frame.pack()

        ########################################################################
        ### Clicking unhappy prints the number of blue and red neighbours
        ### and indicates unhappy cells with "X".
        ### This is used only for testing.
        ########################################################################
        button = Button(frame, text = "Random", command = self.randomBoard).grid(row = 1, column = 1)
        button = Button(frame, text = "Unhappy", command = self.unhappy).grid(row = 1, column = 2)
        button = Button(frame, text = "Move unhappy", command = self.moveUnhappy).grid(row = 1, column = 3)
        button = Button(frame, text = "Start", command = self.start).grid(row = 1, column = 4)

        root.mainloop()

    def printCell(self, i, j):
        self.canvas.create_rectangle(j * self.cellSize, i * self.cellSize,
                                     (j + 1) * self.cellSize, (i + 1) * self.cellSize,
                                     fill = self.population[i, j])

    def printBoard(self):
        for i, j in self.population:
            self.printCell(i, j)

    def leftButton(self, event):
        i, j = int(event.y / self.cellSize), int(event.x / self.cellSize)
        self.population[i, j] = "red"
        self.printCell(i, j)
        
    def leftDoubleButton1(self, event):
        i, j = int(event.y / self.cellSize), int(event.x / self.cellSize)
        self.population[i, j] = "blue"
        self.printCell(i, j)

    def rightButton(self, event):
        i, j = int(event.y / self.cellSize), int(event.x / self.cellSize)
        self.population[i, j] = "white"
        self.printCell(i, j)

    ### Create a random population.
    def randomBoard(self):
        for i, j in self.population:
            self.population[i, j] = random.choice(['red', 'blue', 'white'])
        self.printBoard()

    def unhappy(self):
        for (i, j) in self.population:
            if (i, j) in self.process.populatedCells():
                self.canvas.create_text(self.cellSize * (j + 0.25),
                                    self.cellSize * (i + 0.25),
                                    text = "b: " + str(self.process.typesOfNeighbours(i, j)[0]),
                                    font = "Times 12")
                self.canvas.create_text(self.cellSize * (j + 0.25),
                                    self.cellSize * (i + 0.75),
                                    text = "r: " + str(self.process.typesOfNeighbours(i, j)[1]),
                                    font = "Times 12")
                if (i, j) in self.process.unsatisfiedCells():
                    self.canvas.create_text(self.cellSize * (j + 0.75),
                                    self.cellSize * (i + 0.5),
                                    text = "X",
                                    font = "Times 12")

    def moveUnhappy(self):
        self.process.moveUnsatisfied()
        self.printBoard()

    def start(self):
        ### The board stabilizes quite fast. For 20 x 20, 20 iterations is too much.
        for i in range(20):
            self.process.moveUnsatisfied()
            self.printBoard()
            self.canvas.update()
            self.canvas.after(500)
        self.canvas.create_text(200, 200, text = "Finished", font = "Times 48")




NeighboursSimulation(True)

