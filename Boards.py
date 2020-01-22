'''Some representations of simple boards.
Use the second class to build a sliding puzzle.
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
    ### The first one returns all the elements in the surrounding square.
    ### The second one requires that the cells share a common side.
    ### So (0, 0) and (1, 1) are neighbours by the first but not by the second method.

    def getNeighboursFull(self, i, j):
        neighbours = {(i + k, j + l) for k in range(-1, 2) for l in range(-1, 2)}
        ### The element (i, j) is contained in the above set.
        neighbours.remove((i, j))
        ### The set neighbours might still contain negative indices.
        return neighbours & self.cells

    def getNeighbours(self, i, j):
        remove = {(i + k, j + l) for k in range(-1, 2) for l in range(-1, 2) if k * l != 0}
        return self.getNeighboursFull(i, j) - remove

    def swapObjects(self, i, j, k, l):
        if (i, j) in self.population and (k, l) in self.population:
            self.population[i, j], self.population[k, l] = self.population[k, l], self.population[i, j]




class SlidingPuzzle(SimpleBoard):
    """ This class represents a sliding puzzle. It has numbers from 1 to rows * columns - 1,
        and the largest number (lower right corner of the board) represents the blank piece.
    """
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        ### Initialize the board; the largest number represents the blank piece.
        self.population = {(i, j) : i * self.columns + j + 1   for i in range(self.rows)
                                                               for j in range(self.columns)}
        self.positionOfBlank = (self.rows - 1, self.columns - 1)
        ### Copy the initial position as a solution.
        self.solution = dict(self.population)

    def getSolution(self):
        return self.solution

    def getPositions(self):
        return self.population
    
    def findBlankPiece(self):
        return self.positionOfBlank

    ### Shuffle the board by randomly choosing neighbours of the blank piece.
    
    def shuffle(self):
        for k in range(10000):
            now = self.findBlankPiece()
            new = random.choice(tuple(self.getNeighbours(*now)))
            self.swapObjects(*now, *new)
            self.positionOfBlank = new
        return self.population
    
    ### Provide methods to change the positions of several pieces with one click.
    
    def movePiecesInRow(self, row, positionOfBlank, index):
        ### Check if the blank piece moves from left to right or vice versa
        order = 1 if positionOfBlank < index else -1
        for i in range(positionOfBlank, index, order):
            self.swapObjects(row, i, row, i + order)
        self.positionOfBlank = (row, index)

    def movePiecesInColumn(self, column, positionOfBlank, index):
        ### Blank goes up or down?
        order = 1 if positionOfBlank < index else -1
        for i in range(positionOfBlank, index, order):
            self.swapObjects(i, column, i + order, column)
        self.positionOfBlank = (index, column)




################################################################
######## Something under construction...
################################################################            




"""
class Block:
    #### Threshold indicates ho many similar neighbours a block needs to be satisfied.
    def __init__(self, colour, threshold):
        self.colour = colour
        self.threshold = threshold

    def isSatisfied(self, similarNeighbours):
        return similarNeighbours >= self.threshold

    #### For testing
    def __str__(self):
        return(f"Colour: {self.colour}, Thr: {self.threshold}")




class MovingBlocks(SimpleBoard):
    #### Represents a population of blocks living on a board.
    #### An unsatisfied block moves to another position on the board.
    def __init__(self, rows, columns, population = None):
        super().__init__(rows, columns, population)

    def populatedCells(self):
        return set(self.population.keys())

    def emptyCells(self):
        return self.cells - populatedCells()

    ### Override neighbours to return only populated neighbouring cells
    def getNeighboursFull(self, i, j):
        neighbourCells = super().getNeighboursFull(i, j)
        populatedNeighbourCells = neighbourCells & self.populatedCells()
        return {(k, l): self.population[k, l] for (k, l) in neighbourCells if (k, l) in self.population}

    def isSatisfied(self, i, j):
        if (i, j) in self.population:
            colour = self.population[i, j].colour
            neighbour_colours = [self.items[k, l].colour for k, l in self.neighbours(i, j)]
            if neighbour_colours:
                count = neighbour_colours.count(colour)
                return count >= self.items[i, j].threshold
            else:
                return False

    def satisfiedCells(self):
        return {(i, j) for (i, j) in self.items if self.isSatisfied(i, j)}

    def unsatisfiedCells(self):
        return self.populatedCells() - self.satisfiedCells()

    def closestEmptyCells(self, i, j):
        minDist = min({dist1(i, j, k, l) for k, l in self.emptyCells()})
        return {(k,l) for k, l in self.emptyCells() if dist1(i, j, k, l) == minDist}

    def move(self, i, j):
        #### Move a block at the position (i, j) to a closest empty cell.
        new_cell = random.choice(tuple(self.closestEmptyCells(i, j)))
        self.items[new_cell] = self.items[i, j]
        del self.items[i, j]

    def moveUnsatisfied(self):
        for i, j in self.unsatisfiedCells():
            self.move(i, j)
"""


