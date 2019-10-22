''' This game shows a sequence of numbers and asks what number was shown,
say, 3 times ago. The player may adjust this lag between 3-6, choose
whether numbers 0-1 or 0-9 are shown, and the available time to give answers.
The answers are given using a keyboard.'''

import random
import time
import tkinter as tk

class memoryGame:
    def __init__(self):
        window = tk.Tk()
        window.title("Testaa muistiasi!")
        self.lag = 3
        self.usedNumbers = 1
        self.answerTime = 2

        # Create a menu bar
        menubar = tk.Menu(window)
        window.config(menu = menubar)

        # Create a menu for the lag
        lagMenu = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "Viive", menu = lagMenu)
        lagMenu.add_command(label = "3", command = lambda: self.changeLag(3))
        lagMenu.add_command(label = "4", command = lambda: self.changeLag(4))
        lagMenu.add_command(label = "5", command = lambda: self.changeLag(5))

        # Create a menu for the used numbers
        numberMenu = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "Numerot", menu = numberMenu)
        numberMenu.add_command(label = "0-1", command = lambda: self.changeNumber(1))
        numberMenu.add_command(label = "0-9", command = lambda: self.changeNumber(9))

        # Create a menu for time
        timeMenu = tk.Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "Aika", menu = timeMenu)
        timeMenu.add_command(label = "1.0 s", command = lambda: self.changeTime(1))
        timeMenu.add_command(label = "2.0 s", command = lambda: self.changeTime(2))
        timeMenu.add_command(label = "3.0 s", command = lambda: self.changeTime(3))
        
        # Create a frame to show the chosen options
        frameOptions = tk.Frame(window)
        frameOptions.pack()
        self.labelLag = tk.Label(frameOptions, text = "Viive: " + str(self.lag))
        self.labelNum = tk.Label(frameOptions, text = "Numerot: 0-" + str(self.usedNumbers))
        self.labelTime = tk.Label(frameOptions, text = "Aika: " + str(self.answerTime) + ' s')
        self.labelLag.grid(row = 1, column = 1)
        self.labelNum.grid(row = 1, column = 2)
        self.labelTime.grid(row = 1, column = 3)

        #### Create an area to show the numbers
        self.canvas = tk.Canvas(window, width = 400, height = 300, bg = "white")
        self.canvas.pack()
        self.canvas.bind("<Key>", self.processKeyEvent)
        self.canvas.focus_set()

        #### Create a frame for the start button
        frame2 = tk.Frame(window)
        frame2.pack()
        startButton = tk.Button(frame2, text = "Aloita", command = self.playGame)
        startButton.pack()

        window.mainloop()

    def playGame(self):
        count = 0
        #### Store the shown numbers
        numbers = []
        correct = True
        #### If several games are played
        self.canvas.delete("text")
        
        while correct:
            k = str(random.randint(0,self.usedNumbers))
            numbers.append(k)
            self.canvas.create_text(200, 150, text = k, font = "Times 96", tags = "text")
            self.canvas.update()
            self.canvas.after(self.answerTime * 1000)
            self.canvas.delete("text")
            self.canvas.update()
            self.canvas.after(self.answerTime * 500)

            if count >= self.lag - 1:
                self.answer = ''
                self.canvas.create_text(200, 100, text = str(count - self.lag + 2) + ". numero oli:",
                                            font = "Times 36", tags = "text")
                self.canvas.update()
                self.canvas.after(self.answerTime * 1000)
                self.canvas.delete("text")
                self.canvas.update()
                
                correct = self.answer == numbers[0]
                numbers = numbers[1: ]
                self.canvas.after(500)
            count += 1

        #### The game ends: flash red and black screen and print the score
        for i in range(3):
            self.canvas["bg"] = "red"
            self.canvas.update()
            self.canvas.after(250)
            self.canvas["bg"] = "black"
            self.canvas.update()
            self.canvas.after(250)

        self.canvas["bg"] = "white"
        self.canvas.create_text(200, 150, text = "Pisteet: " + str(count-self.lag),
                                font = "Times 36", tags = "text")

    def changeLag(self, n):
        self.lag = n
        self.labelLag["text"] = "Viive: " + str(self.lag)

    def changeTime(self, n):
        self.answerTime = n
        self.labelTime["text"] = "Aika: " + str(self.answerTime) + ' s'

    def changeNumber(self, n):
        self.usedNumbers = n
        self.labelNum["text"] = "Numerot: 0-" + str(n)
        
    def processKeyEvent(self, event):
        self.answer = event.keysym

memoryGame()            
