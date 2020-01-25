'''Two versions of a sliding puzzle. When a piece is in a correct position,
it is shown with green background. The extreme version of the game does
not show the numbers in the pieces. A player may use hints by
pressing h on the keyboard. The smallest number on the board in
incorrect position is shown.
'''


import tkinter as tk
import tkinter.messagebox
from Boards import SlidingPuzzle


class SlidingPuzzleCanvas(tk.Canvas):
    def __init__(self, container, rows, columns, showNumbers = True):
        self.rows = rows
        self.columns = columns
        self.puzzle = SlidingPuzzle(self.rows, self.columns)
        self.solution = self.puzzle.getSolution()
        self.showNumbers = showNumbers
        self.clicks = 0

        ### Initial values for the canvas
        
        self.cellSizeX = self.cellSizeY = 50
        self.canvasSizeX = self.cellSizeX * self.columns
        self.canvasSizeY = self.cellSizeY * self.rows
        self.fontsize = int(0.5 * min(self.cellSizeX, self.cellSizeY))

        self.canvas = tk.Canvas(container, width = self.canvasSizeX,
                                height = self.canvasSizeY, bg = "gray")
        self.canvas.pack(expand = True, fill = 'both')
        
        self.canvas.bind("<Button-1>", self.processMouseClick)
        self.canvas.bind("<Configure>", self.changeSize)
        self.canvas.bind("h", self.showHint)
        self.canvas.focus_set()

        self.puzzle.shuffle()
        self.printPuzzle(self.puzzle.getPositions())

        container.mainloop()

    def printPiece(self, i, j):
        xCoord = j * self.cellSizeX
        yCoord = i * self.cellSizeY
        isBlank = (i, j) == self.puzzle.findBlankPiece()
        isCorrect = self.solution[i, j] == self.puzzle.getPositions()[i, j]

        if isBlank:
            self.canvas.create_rectangle(xCoord, yCoord,
                                         xCoord + self.cellSizeX, yCoord + self.cellSizeY,
                                         fill = "black",
                                         tag = "piece")
        if not isBlank:
            self.canvas.create_rectangle(xCoord, yCoord,
                                         xCoord + self.cellSizeX, yCoord + self.cellSizeY,
                                         fill = "green" if isCorrect else "gray",
                                         tag = "piece")
            ### Extreme version of the game does not show numbers,
            ### only whether some piece is in a correct position.
            if self.showNumbers:
                self.canvas.create_text(xCoord + self.cellSizeX / 2, yCoord + self.cellSizeY / 2,
                                        text = str(self.puzzle.getPositions()[i, j]),
                                        font = f"Times {self.fontsize}",
                                        tag = "text")

    def printPuzzle(self, board):
        self.canvas.delete("piece")
        self.canvas.delete("text")
        for i, j in board:
            self.printPiece(i, j)

    def clickedCell(self, xCoord, yCoord):
        ### Get the sell which contains the point (xCoord, yCoord)
        return int(yCoord / self.cellSizeY), int(xCoord / self.cellSizeX)
        

    def processMouseClick(self, event):
        if not self.showNumbers:
            self.canvas.delete("text")
        i, j = self.clickedCell(event.x, event.y)
        m, n = self.puzzle.findBlankPiece()
        ### A valid click happens on the same row or column with the blank piece.
        ### Count only valid clicks.
        if i == m:
            self.clicks += 1
            self.puzzle.movePiecesInRow(i, n, j)
            ### Print only the moved pieces, not the full board
            for k in range(min(n, j), max(n, j) + 1):
                self.printPiece(i, k)
        if j == n:
            self.clicks += 1
            self.puzzle.movePiecesInColumn(j, m, i)
            ### Print only the moved pieces, not the full board
            for k in range(min(i, m), max(i, m) + 1):
                self.printPiece(k, j)

        if self.puzzle.getPositions() == self.solution:
            self.canvas.delete("all")
            self.canvas.create_text(self.canvasSizeX / 2, self.canvasSizeY / 2,
                                    text = str(self.clicks) + " clicks",
                                    font = f"Times {self.fontsize}",
                                    tag = "solved")

    def changeSize(self, event):
        self.cellSizeX = int(event.width / self.columns)
        self.cellSizeY = int(event.height / self.rows)
        self.canvasSizeX = self.cellSizeX * self.columns
        self.canvasSizeY = self.cellSizeY * self.rows
        self.fontsize = int(0.5 * min(self.cellSizeX, self.cellSizeY))
        ### The size of the board changes, so print the full board.
        self.printPuzzle(self.puzzle.getPositions())

    def showHint(self, event):
        i, j = self.puzzle.hint()[0],self.puzzle.hint()[1] 
        xCoord = j * self.cellSizeX
        yCoord = i * self.cellSizeY
        self.canvas.create_text(xCoord + self.cellSizeX / 2, yCoord + self.cellSizeY / 2,
                                        text = str(self.puzzle.getPositions()[i, j]),
                                        font = f"Times {self.fontsize}",
                                        tag = "text")




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
        self.showNumbers = 1 - self.check.get()

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
        columns = self.choice1.get()
        rows = self.choice2.get()
        if 3 <= rows <= 10 and 3 <= columns <= 10:
            game = tk.Toplevel()
            game.title(str(rows) + " X " + str(columns))
            extreme = 1 - self.check.get()
            gameCanvas = SlidingPuzzleCanvas(game, rows, columns, extreme)
            # if extreme:
            #     FrameHint = tk.Frame(game)
            #     FrameHint.pack()
            #     tk.Button(FrameHint, text = "Hint", command = self.clickStart).pack()
        else:
            tkinter.messagebox.showerror("Error", "Give proper values!")


SlidingPuzzleGame()

