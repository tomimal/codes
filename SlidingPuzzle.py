'''Two versions of a sliding puzzle. When a piece is in a correct position,
it is shown with green background. The extreme version of the game does
not show the numbers in the pieces. A player may use hints by
pressing h on the keyboard. The smallest number on the board in
incorrect position is shown.

FIX: If the player clicks at the right upper corner after the game ends,
the game continues.
'''


import tkinter as tk
from Boards import SlidingPuzzle


class SlidingPuzzleNormal(tk.Canvas):
    def __init__(self, container, rows, columns):
        self.container = container
        self.rows = rows
        self.columns = columns
        self.puzzle = SlidingPuzzle(self.rows, self.columns)
        ### Count how many clicks a player needs to solve the puzzle.
        self.clicks = 0

        ### Initial values for the canvas
        
        self.cellSizeX = self.cellSizeY = 50
        self.canvasSizeX = 50 * self.columns
        self.canvasSizeY = 50 * self.rows
        self.fontsize = int(self.cellSizeX / 2)

        self.canvas = tk.Canvas(self.container,
                                width = self.canvasSizeX,
                                height = self.canvasSizeY,
                                bg = "gray")
        self.canvas.pack(expand = True, fill = 'both')
        
        self.canvas.bind("<Button-1>", self.leftClick)
        self.canvas.bind("<Configure>", self.changeSize)

        self.puzzle.shuffle()
        self.printPuzzle()

    def printPiece(self, i, j):
        ### Find the coordinates of the upper left corner of the cell at (i, j)
        xCoord = j * self.cellSizeX
        yCoord = i * self.cellSizeY
        ### A piece (not blank) at the correct position is shown green.
        if (i, j) == self.puzzle.getPositionOfBlank():
            colour = "black"
        elif self.puzzle.isCorrect(i, j):
            colour = "green"
        else:
            colour = "gray"

        self.canvas.create_rectangle(xCoord, yCoord,
                                     xCoord + self.cellSizeX, yCoord + self.cellSizeY,
                                     fill = colour, tag = "piece")

    def printNumber(self, i, j):
        xCoord = j * self.cellSizeX
        yCoord = i * self.cellSizeY
        number = self.puzzle.getPositions()[i, j]
        self.canvas.create_text(xCoord + self.cellSizeX / 2, yCoord + self.cellSizeY / 2,
                                text = number,
                                font = f"Times {self.fontsize}",
                                tag = "text")

    def printPuzzle(self):
        self.canvas.delete("all")
        for i, j in self.puzzle.getPositions():
            self.printPiece(i, j)
            self.printNumber(i, j)

    def clickedCell(self, xCoord, yCoord):
        ### A click at the lower or right boundary would produce
        ### a non-existent cell; min takes care of this.
        row = min(int(yCoord / self.cellSizeY), self.rows - 1)
        col = min(int(xCoord / self.cellSizeX), self.columns - 1)
        return row, col

    def leftClick(self, event):
        i, j = self.clickedCell(event.x, event.y)
        m, n = self.puzzle.getPositionOfBlank()
        
        ### Count only valid clicks (same row or column with the blank piece).
        if i == m or j == n:
            self.clicks += 1
            self.puzzle.movePieces((i, j))
            self.printPuzzle()

        if self.puzzle.isSolved():
            self.printResult()

    def printResult(self):
        self.canvas.delete("all")
        self.canvas.create_text(self.canvasSizeX / 2, self.canvasSizeY / 2,
                                text = str(self.clicks) + " clicks",
                                font = f"Times {self.fontsize}",
                                tag = "solved")

    def changeSize(self, event):
        self.canvasSizeX, self.canvasSizeY = event.width, event.height
        self.cellSizeX = int(event.width / self.columns)
        self.cellSizeY = int(event.height / self.rows)
        self.fontsize = int(0.5 * min(self.cellSizeX, self.cellSizeY))
        self.printPuzzle()




class SlidingPuzzleExtreme(SlidingPuzzleNormal):
    def __init__(self, container, rows, columns):
        SlidingPuzzleNormal.__init__(self, container, rows, columns)

        ### Provide hints in this game.
        self.canvas.bind("h", self.showHint)
        self.canvas.focus_set()

    def printPuzzle(self):
        self.canvas.delete("all")
        for i, j in self.puzzle.getPositions():
            self.printPiece(i, j)

    def leftClick(self, event):
        ### Erase a hint when the mouse button is clicked.
        self.canvas.delete("text")
        SlidingPuzzleNormal.leftClick(self, event)

    def showHint(self, event):
        i, j = self.puzzle.hint()[0], self.puzzle.hint()[1]
        self.printNumber(i, j)




### Create an actual game


import tkinter.messagebox


class SlidingPuzzleGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sliding Puzzle")

        frame = tk.Frame(self.window)
        frame.pack()
        text1 = tk.Label(frame, text = "Width 3 - 10: ")
        self.choice1 = tk.IntVar()
        entry1 = tk.Entry(frame, textvariable = self.choice1)
        text2 = tk.Label(frame, text = "Height 3 - 10: ")
        self.choice2 = tk.IntVar()
        entry2 = tk.Entry(frame, textvariable = self.choice2)
        self.check = tk.IntVar()
        check = tk.Checkbutton(frame, text = "Extreme", variable = self.check)

        text1.grid(row = 1, column = 1)
        entry1.grid(row = 1, column = 2)
        text2.grid(row = 1, column = 3)
        entry2.grid(row = 1, column = 4)
        check.grid(row = 1, column = 5)

        FrameStart = tk.Frame(self.window)
        FrameStart.pack()
        tk.Button(FrameStart, text = "Start", command = self.clickStart).pack()

        self.window.mainloop()

    def clickStart(self):
        cols = self.choice1.get()
        rows = self.choice2.get()
        if 3 <= rows <= 10 and 3 <= cols <= 10:
            game = tk.Toplevel()
            game.title(str(rows) + " X " + str(cols))
            if self.check.get():
                SlidingPuzzleExtreme(game, rows, cols)
            else:
                SlidingPuzzleNormal(game, rows, cols)
        else:
            tkinter.messagebox.showerror("Error", "Give proper values!")


SlidingPuzzleGame()

