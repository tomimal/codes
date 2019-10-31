'''A sliding puzzle. A class of sequences which handles the parity of
permutations is defined. A sliding puzzle is represented as a
dictionary. tkInter is used to show the game.

Coming up:  Display something when the puzzle is solved (time, number of clicks)
            Possibility to move several pieces with one click'''


from random import shuffle
import tkinter as tk


class OwnList(list):
    '''A class to check the parity of a sequence.
    '''

    def numberOfInversions(self):
        ans = sum([1 for i in range(len(self)) for j in range(i + 1, len(self))
                   if self[i] > self[j]])
        return ans

    def isEven(self):
        return self.numberOfInversions() % 2 == 0


class Board:
    '''A square board: pieces is a dictionary of the form {(i, j): number},
    where (i, j) is the position of some piece.
    Method shuffle_board checks that the resulting game is solvable.
    '''
    def __init__(self, size, pieces):
        self.size = size
        self.pieces = pieces

    def get_neighbours(self, i, j):
        neighbours = []
        if i > 0:
            neighbours.append((i - 1, j))
        if i < self.size - 1:
            neighbours.append((i + 1, j))
        if j > 0:
            neighbours.append((i, j - 1))
        if j < self.size - 1:
            neighbours.append((i, j + 1))
        return neighbours

    def shuffle_board(self):
        numbers = OwnList(range(1, self.size ** 2 + 1))
        if self.size % 2 == 1:
            solvable = False
            while not solvable:
                shuffle(numbers)
                check = OwnList([i for i in numbers if i < self.size ** 2])
                solvable = check.isEven()
            for i in range(self.size):
                for j in range(self.size):
                    self.pieces[i, j] = numbers[j + i * self.size]
        else:
            solvable = False
            while not solvable:
                shuffle(numbers)
                check = OwnList([i for i in numbers if i < self.size ** 2])
                row_of_blank = (numbers.index(self.size ** 2) // self.size) % 2
                solvable = (check.isEven() and row_of_blank == 0) or \
                           (not check.isEven() and row_of_blank == 1)
            for i in range(self.size):
                for j in range(self.size):
                    self.pieces[i, j] = numbers[j + i * self.size]
        return Board(self.size, self.pieces)
        
    def swap_pieces(self, i_0, j_0, i_1, j_1):
        self.pieces[i_0, j_0], self.pieces[i_1, j_1] = self.pieces[i_1, j_1], self.pieces[i_0, j_0]
        return Board(self.size, self.pieces)


class Game:
    def __init__(self, size = 9):
        self.size = size

        window = tk.Tk()
        window.title = "Puzzle"

        self.canvas_size_x = 400
        self.canvas_size_y = 400
        self.cell_size = int(self.canvas_size_x / self.size)
        self.fontsize = int(0.5 * self.cell_size)
        #### This number represents the blank piece
        self.blank = self.size ** 2

        #### Create a solved puzzle
        self.ordered_pieces = {(i,j): i * self.size + j + 1
                               for i in range(self.size)
                               for j in range(self.size)}
        self.board = Board(self.size, self.ordered_pieces)

        #### Create canvas for the game
        self.canvas = tk.Canvas(window, width = self.canvas_size_x,
                                height = self.canvas_size_y, bg = "gray")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.processMouseClick)
        self.canvas.focus_set()

        #### Create a frame for the shuffle button
        FrameShuffle = tk.Frame(window)
        FrameShuffle.pack()
        StartButton = tk.Button(FrameShuffle, text = "Shuffle", command = self.start_game).pack()
        
        self.print_board(self.board)

        window.mainloop()

    def print_piece(self, i, j):
        number = self.ordered_pieces[i, j]
        y_coord = i * self.cell_size
        x_coord = j * self.cell_size
        if number < self.blank:
            self.canvas.create_rectangle(x_coord, y_coord,
                                         x_coord + self.cell_size, y_coord + self.cell_size)
            self.canvas.create_text(x_coord + self.cell_size / 2, y_coord + self.cell_size / 2,
                                    text = str(number), font = f"Times {self.fontsize}", tag = "piece")
        else:
            self.canvas.create_rectangle(x_coord, y_coord,
                                         x_coord + self.cell_size, y_coord + self.cell_size,
                                         fill = "black", tag = "piece")

    def print_board(self, board):
        self.canvas.delete("piece")
        for i, j in self.ordered_pieces.keys():
            self.print_piece(i, j)

    def start_game(self):
        self.print_board(self.board.shuffle_board())

    def processMouseClick(self, event):
        #### Find the position of the clicked piece
        i = int(event.y // self.cell_size)
        j = int(event.x // self.cell_size)
        
        #### Check if one of the neighbours of the clicked piece is blank
        neighbour_positions = self.board.get_neighbours(i, j)
        for k, l in neighbour_positions:
            if self.board.pieces[k, l] == self.blank:
                self.board.swap_pieces(i, j, k, l)
                self.print_board(self.board)



Game()
