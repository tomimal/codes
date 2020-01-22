'''A sliding puzzle.

Coming up:  Fix the messge after the game ends.
            Take care of size of the canvas etc.
            Add that pieces in correct positions have different colour.

            FIX: If a player clicks in the canvas but outside of
            all the cells, the piece is not found from the dictionary
            and this causes an error. (Depends on the size of canvas.)
'''


import tkinter as tk
from Boards import SlidingPuzzle


class SlidingPuzzleGame:
    def __init__(self, rows = 8, columns = 8):
        self.rows = rows
        self.columns = columns
        self.puzzle = SlidingPuzzle(self.rows, self.columns)
        self.solution = self.puzzle.getSolution()
        self.clicks = 0

        window = tk.Tk()
        window.title("Sliding Puzzle")

        self.canvasSizeX = 400
        self.canvasSizeY = 400
        self.cellSize = int(self.canvasSizeX / max(self.rows, self.columns))
        self.fontsize = int(0.5 * self.cellSize)

        self.canvas = tk.Canvas(window, width = self.canvasSizeX,
                                height = self.canvasSizeY, bg = "gray")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.processMouseClick)

        ### Create a frame for the shuffle button
        FrameShuffle = tk.Frame(window)
        FrameShuffle.pack()
        tk.Button(FrameShuffle, text = "Shuffle",
                  command = lambda : self.printPuzzle(self.puzzle.shuffle())).pack()

        ### Display the solved puzzle
        self.printPuzzle(self.solution)

        window.mainloop()

    def printPiece(self, i, j):
        yCoord = i * self.cellSize
        xCoord = j * self.cellSize
        isBlank = (i, j) == self.puzzle.findBlankPiece()

        self.canvas.create_rectangle(xCoord, yCoord,
                                     xCoord + self.cellSize, yCoord + self.cellSize,
                                     fill = "black" if isBlank else "gray",
                                     tag = "piece")
        if not isBlank:
            self.canvas.create_text(xCoord + self.cellSize / 2, yCoord + self.cellSize / 2,
                                    text = str(self.puzzle.getPositions()[i, j]),
                                    font = f"Times {self.fontsize}",
                                    tag = "piece")

    def printPuzzle(self, board):
        self.canvas.delete("piece")
        for i, j in board:
            self.printPiece(i, j)

    def processMouseClick(self, event):
        #### Find the position of the clicked piece
        i = int(event.y // self.cellSize)
        j = int(event.x // self.cellSize)
        m, n = self.puzzle.findBlankPiece()
        if i == m:
            ### Count only valid clicks
            self.clicks += 1
            self.puzzle.movePiecesInRow(i, n, j)
            for k in range(min(n, j), max(n, j) + 1):
                self.printPiece(i, k)
        if j == n:
            ### Count only valid clicks
            self.clicks += 1
            self.puzzle.movePiecesInColumn(j, m, i)
            for k in range(min(i, m), max(i, m) + 1):
                self.printPiece(k, j)

        if self.puzzle.population == self.solution:
            self.canvas.delete("all")
            self.canvas.create_text(200, 200,
                                    text = "Solved:\n" + str(self.clicks) + " clicks",
                                    font = f"Times {self.fontsize}",
                                    tag = "piece")



SlidingPuzzleGame()
