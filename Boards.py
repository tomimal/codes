'''Some representations of simple boards.
The second class represents a sliding puzzle.
'''


import random


class SimpleBoard:
    """ Population is a dictionary (see method swapObjects) of objects on the board.
    """
    def __init__(self, rows, columns, population = None):
        self.rows = rows
        self.columns = columns
        self.population = population
        self.cells = {(i, j) for i in range(self.rows) for j in range(self.columns)}

    ### Provide two methods to get the neighbours of a cell.
    ### The first one returns all the cells in the surrounding square.
    ### The second one requires that the cells share a common side.
    ### For example, (0, 0) and (1, 1) are neighbours by the first but not by the second method.

    def getNeighboursFull(self, i, j):
        neighbours = {(i + k, j + l) for k in range(-1, 2)
                                     for l in range(-1, 2)}
        ### A cell is not a neighbour of itself.
        neighbours.remove((i, j))
        ### The set neighbours might contain negative indices.
        return neighbours & self.cells

    def getNeighbours(self, i, j):
        remove = {(i + k, j + l) for k in range(-1, 2) for l in range(-1, 2) if k * l != 0}
        return self.getNeighboursFull(i, j) - remove

    def swapObjects(self, i, j, k, l):
        self.population[(i, j)], self.population[(k, l)] = self.population[(k, l)], self.population[(i, j)]




class SlidingPuzzle(SimpleBoard):
    """ The class represents a sliding puzzle. It has numbers from 1 to rows * columns,
        and the largest number (rows * columns) represents the blank piece.
    """
    def __init__(self, rows, columns):
        SimpleBoard.__init__(self, rows, columns)
        ### Initialize the board; the largest number represents the blank piece.
        ### self.population represents the current board (it changes after clicks).
        self.population = {(i, j) : i * self.columns + j + 1   for i in range(self.rows)
                                                               for j in range(self.columns)}
        ### The initial board is the solution.
        self.solution = dict(self.population)

    def isCorrect(self, i, j):
        return self.population[i, j] == self.solution[i, j]

    def isSolved(self):
        return self.solution == self.population

    def getPositions(self):
        return self.population
    
    def getPositionOfBlank(self):
        ### One could keep track of the blank piece using a variable.
        ### This should be updated in the methods shuffle and movePieces,
        ### but in this small board the following search will not take long.
        for (i, j) in self.population:
            if self.population[i, j] == self.rows * self.columns:
                return (i, j)

    ### Shuffle the board by randomly choosing neighbours of the blank piece.
    ### Maximum size of the board will be 10 x 10, so 10,000 should be enough.
    
    def shuffle(self):
        for k in range(10000):
            now = self.getPositionOfBlank()
            new = random.choice(tuple(self.getNeighbours(*(now))))
            self.swapObjects(*(now), *(new))

    ### Change the positions of several pieces with one click.
    
    def movePieces(self, clicked):
        rowBlank, colBlank = self.getPositionOfBlank()
        rowClick, colClick = clicked

        ### Check if the blank piece and the clicked piece are in the same row. 
        if rowBlank == rowClick:
            ### Check if the blank piece moves from left to right or vice versa
            order = 1 if colBlank < colClick else -1
            for i in range(colBlank, colClick, order):
                self.swapObjects(rowBlank, i, rowBlank, i + order)

        ### Check if the blank piece and the clicked piece are in the same column.
        if colBlank == colClick:
            ### Check if the blank piece moves from up to down or vice versa
            order = 1 if rowBlank < rowClick else -1
            for i in range(rowBlank, rowClick, order):
                self.swapObjects(i, colBlank, i + order, colBlank)

    ### The actual game will contain an extreme mode where the numbers
    ### in the pieces are not shown.
    ### Find the position of the smallest number on the board
    ### which is not in a correct position.
    
    def hint(self):
        number = self.rows * self.columns
        for (i, j) in self.population:
            if not self.isCorrect(i, j) and self.population[i, j] < number:
                number = self.population[i, j]
                position = (i, j)
        return position




################################################################
######## Under construction...
########
######## FIX: The isSatisfied method now uses fixed threshold of 0.5    
################################################################            




class MovingItems(SimpleBoard):
    """ Represents a population (of two colours) living on a board.
        Each cell requires a certain amount of similar neighbours to be satisfied.
        Unsatisfied blocks moves to another position on the board.
        Population is meant to be a dictionary (i, j) : red OR blue OR white.
        (i, j) is a cell on the board and white represents unpopulated cell.
    """    
    def __init__(self, rows, columns, population = None):
        SimpleBoard.__init__(self, rows, columns, population)

    def populatedCells(self):
        """ Return the set of populated cells."""
        return {(i, j) for (i, j) in self.population
                       if self.population[i, j] != 'white'}

    def getNeighbours(self, i, j):
        """ Return the set of populated neighbour cells."""
        neighbourCells = SimpleBoard.getNeighboursFull(self, i, j)
        return {(k, l) for (k, l) in neighbourCells if (k, l) in self.populatedCells()}

    def typesOfNeighbours(self, i, j):
        """ Return the number of blue and red neighbours."""
        neghbs = [self.population[k, l] for (k, l) in self.getNeighbours(i, j)]
        return neghbs.count('blue'), neghbs.count('red')

    def isSatisfied(self, i, j):
        ### Else statement applies if (i, j) is a white cell.
        blue = self.typesOfNeighbours(i, j)[0]
        red  = self.typesOfNeighbours(i, j)[1]
        if self.population[i, j] == 'blue':
            return blue >= red
        else:
            return red >= blue

    def unsatisfiedCells(self):
        return {(i, j) for (i, j) in self.populatedCells() if not self.isSatisfied(i, j)}

    def getEmptyCell(self):
        emptyCells = self.cells - self.populatedCells()
        return random.choice(tuple(emptyCells))

    def move(self, i, j):
        """ Move an item to some empty cell."""
        newCell = self.getEmptyCell()
        self.population[newCell] = self.population[i, j]
        self.population[i, j] = 'white'

    def moveUnsatisfied(self):
        for i, j in self.unsatisfiedCells():
            self.move(i, j)

