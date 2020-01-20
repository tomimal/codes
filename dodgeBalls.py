"""" Class MovingBallsCanvas creates an area where a player
moves a red ball using mouse. The area is initialized with two
blue balls (at fixed positions but with random velocities) and the
player clicks on the area to create a red ball. The blue
balls start moving and the player needs to move the red ball
such that it does not hit the blue balls or the boundaries of the area.

Class MovingBallsGame below uses this class to create a game to play.
"""


import tkinter as tk
import tkinter.messagebox
from movingBall import MovingBall
from bouncingObjects import BouncingObjects
import math
import time
import random


def distance(x0,y0,x1,y1):
    return ((x0 - x1) ** 2 + (y0 - y1) ** 2) ** 0.5


def randomAngle():
    return 2 * math.pi * random.random()


class MovingBallsCanvas(BouncingObjects):
    def __init__(self, container, width, height, bg):
        super().__init__(container, width, height, bg)
        self.gameHasStarted = False

        ### Use the same radius for all the balls. If the red ball
        ### has a different radius, methods mouseClick and
        ### redBallHitsBlueBall need to be modified.
        ### self.velocity is the initial velocity of the blue balls.
        ### self.changeSpeed gives the probability (1/10 here; see increaseSpeed)
        ### that the speed of a blue ball increases when it hit a boundary.
        
        self.radius = 30
        self.speed = 5
        self.changeSpeed = 9

        self.bind("<Button-1>", self.mouseClick)
        self.bind("<B1-Motion>", self.mouseMove)
        self.bind("<ButtonRelease-1>", self.mouseRelease)

        ### Initialize the board with two blue balls with given velocity.
        ### The blue balls move in a randomly chosen direction.

        self.blue1 = MovingBall(int(0.2 * self.width), int(0.2 * self.height),
                                self.radius, self.speed, randomAngle(), "blue")
        self.blue2 = MovingBall(int(0.8 * self.width), int(0.8 * self.height),
                                self.radius, self.speed, randomAngle(), "blue")
        self.blue1.draw(self)
        self.blue2.draw(self)
        self.addObject(self.blue1)
        self.addObject(self.blue2)

    ### The game begins by creating a red ball when a player clicks
    ### on the canvas. It is checked that the red ball fits to the canvas.

    def mouseClick(self, event):
        if (self.radius <= event.x <= self.width - self.radius    and
            self.radius <= event.y <= self.height - self.radius):
                self.gameHasStarted = True
                self.red = MovingBall(event.x, event.y, self.radius, 0, 0, "red")
                self.addObject(self.red)
                self.timeStart = time.time()
                self.play()

    ### The red ball is moved using the mouse while holding button 1 down.
                
    def mouseMove(self, event):
        self.red.move((event.x, event.y))

    ### If the mouse button is released, the game ends.
    ### self.gameHasStarted is true only if the red ball was created, so a
    ### click too close to the boundaries does not cause stopGame() to be called.

    def mouseRelease(self, event):
        if self.gameHasStarted:
            self.stopGame()

    ### The speed of the blue balls increases randomly after they hit the boundaries.

    def increaseSpeed(self):
        for ball in self.objects:
            if (self.objectAtHorizontalBoundary(ball)  or
                self.objectAtVerticalBoundary(ball)):
                if random.randint(0, self.changeSpeed) == 0:
                    ball.speed += 1

    def redBallHitsBlueBall(self):
        x0, y0 = self.red.x, self.red.y
        for ball in self.objects:
            if (ball.colour != "red"    and
                distance(x0, y0, ball.x, ball.y) < 2 * self.radius):
                return True
        return False

    ### The game ends if the red ball hits a blue ball or a boundary.
    
    def play(self):
        while not (self.objectAtHorizontalBoundary(self.red)  or
                   self.objectAtVerticalBoundary(self.red)    or
                   self.redBallHitsBlueBall()):
            self.drawBoard()
            self.increaseSpeed()
        self.stopGame()

    def stopGame(self):
        self.timeElapsed = int(time.time() - self.timeStart)
        self.delete("all")
        self.create_text(self.width / 2, self.height / 2 - 50,
                         text = "Time:", font = "Times 48")
        self.create_text(self.width / 2, self.height / 2 + 50,
                         text = str(self.timeElapsed) + " seconds",
                         font = "Times 48")
        self.update()
        self.after(5000)
        self.destroy()




################################################
######## Create a game.
################################################




class MovingBallsGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title = "Dodge Blue Balls"

        frame = tk.Frame(self.window)
        frame.pack()
        text1 = tk.Label(frame, text = "Width (400-600): ")
        self.choice1 = tk.IntVar()
        entry1 = tk.Entry(frame, textvariable = self.choice1)
        text2 = tk.Label(frame, text = "Height (400-600): ")
        self.choice2 = tk.IntVar()
        entry2 = tk.Entry(frame, textvariable = self.choice2)
        startButton = tk.Button(frame, text = "Start", command = self.clickStart)

        text1.grid(row = 1, column = 1)
        entry1.grid(row = 1, column = 2)
        text2.grid(row = 1, column = 3)
        entry2.grid(row = 1, column = 4)
        startButton.grid(row = 1, column = 5)

        self.window.mainloop()

    def clickStart(self):
        width = self.choice1.get()
        height = self.choice2.get()
        if 400 <= width <= 600 and 400 <= height <= 600:
            MovingBallsCanvas(self.window, width, height, "grey").pack()
        else:
            tkinter.messgebox.showerror("Error", "Give proper values!")


MovingBallsGame()
