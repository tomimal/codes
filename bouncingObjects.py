"""" Create a class to animate moving and bouncing objects on a canvas.
The class accepts any iterable of objects to animate.
The class assumes that each object has the following methods:

draw(canvas)    Aim: draw the object on a canvas.

move()          Aim: describe how the object moves.

bounds()        returns a sequence (x_0,y_0,x_1,y_1).
                Aim: (x_0, y_0) and (x_1, y_1) are the upper
                left corner and the lower right corner of the 
                smallest rectangle (sides parallel to x-axis
                and y-axis) containing the object.

hitHorizontalLine()     Aim: describe how the object behaves if
hitVerticalLine()       it hits a boundary of the canvas.
"""


import tkinter as tk


class BouncingObjects(tk.Canvas):
    def __init__(self, container, width, height, bg, objects = None):
        super().__init__(container, width = width, height = height, bg = bg)
        self.width = width
        self.height = height
        self.objects = list(objects) if objects else []

        self.sleepTime = 20

    def addObject(self, object):
        self.objects.append(object)

    def drawObjects(self):
        for object in self.objects:
            object.draw(self)

    ### Check if an object hits a boundary.

    def objectAtHorizontalBoundary(self, object):
        return object.bounds()[1] <= 0 or object.bounds()[3] >= self.height

    def objectAtVerticalBoundary(self, object):
        return object.bounds()[0] <= 0 or object.bounds()[2] >= self.width

    ### Each object knows how to move and behave if it hits a boundary.

    def moveObjects(self):
        for object in self.objects:
            object.move()

    def hitBoundaries(self):
        for object in self.objects:
            if self.objectAtHorizontalBoundary(object):
                object.hitHorizontalLine()
            if self.objectAtVerticalBoundary(object):
                object.hitVerticalLine()

    ### The following method draws the objects once.
    ### In an actual animation, we need some stopping condition.

    def drawBoard(self):
        self.delete("all")
        self.drawObjects()
        self.after(self.sleepTime)
        self.update()
        self.hitBoundaries()
        self.moveObjects()
