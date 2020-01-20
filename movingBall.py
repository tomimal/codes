""" The class represents a moving ball in a plane.
The attributes (speed, angle) describe the velocity
of a ball in polar coordinates.
The class provides methods bounds, hitHorizontalLine,
and hitVerticalLine. The last two methods describe
how the velocity of the ball changes if it bounces back
from a line. The method bounds returns the smallest rectangle
containing the ball: this is used to check if the ball
hits a boundary of some given rectangle-form area.
"""


import math


class MovingBall:
    def __init__(self, x, y, radius, speed, angle, colour):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.angle = angle
        self.colour = colour

    def move(self, moveTo = None):
        if moveTo:
            self.x = moveTo[0]
            self.y = moveTo[1]
        else:
            self.x += self.speed * math.cos(self.angle)
            self.y += self.speed * math.sin(self.angle)

    def bounds(self):
        return [self.x - self.radius, self.y - self.radius,
                self.x + self.radius, self.y + self.radius]

    def draw(self, canvas):
        canvas.create_oval(self.x - self.radius, self.y - self.radius,
                           self.x + self.radius, self.y + self.radius,
                           fill = self.colour)

    def hitHorizontalLine(self):
        self.angle = -self.angle

    def hitVerticalLine(self):
        self.angle = math.pi - self.angle



    
