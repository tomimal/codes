'''A GUI to do quaternion arithmetic.'''

from Quaternions import Quaternion
import tkinter as tk
import tkinter.messagebox

class QuaternionGUI:
    def __init__(self):
        window = tk.Tk()
        window.title("Quaternion arithmetic")
        #### Adjust the number of decimals in the output
        self.fmt = "<.5f"

        label = tk.Label(window, text = "Enter two quaternions")
        label.pack()

        # Create a frame to enter two quaternions
        frameQ = tk.Frame(window)
        frameQ.pack()
        tk.Label(frameQ, text = "Scalar").grid(row = 1, column = 2)
        tk.Label(frameQ, text = "i part").grid(row = 1, column = 3)
        tk.Label(frameQ, text = "j part").grid(row = 1, column = 4)
        tk.Label(frameQ, text = "k part").grid(row = 1, column = 5)

        # Enter the first quaternion
        tk.Label(frameQ, text = "Q1:").grid(row = 2, column = 1)
        self.q1_rcomp = tk.DoubleVar()
        self.q1_icomp = tk.DoubleVar()
        self.q1_jcomp = tk.DoubleVar()
        self.q1_kcomp = tk.DoubleVar()
        tk.Entry(frameQ, textvariable = self.q1_rcomp).grid(row = 2, column = 2)
        tk.Entry(frameQ, textvariable = self.q1_icomp).grid(row = 2, column = 3)
        tk.Entry(frameQ, textvariable = self.q1_jcomp).grid(row = 2, column = 4)
        tk.Entry(frameQ, textvariable = self.q1_kcomp).grid(row = 2, column = 5)

        # Enter the second quaternion
        tk.Label(frameQ, text = "Q2:").grid(row = 3, column = 1)
        self.q2_rcomp = tk.DoubleVar()
        self.q2_icomp = tk.DoubleVar()
        self.q2_jcomp = tk.DoubleVar()
        self.q2_kcomp = tk.DoubleVar()
        tk.Entry(frameQ, textvariable = self.q2_rcomp).grid(row = 3, column = 2)
        tk.Entry(frameQ, textvariable = self.q2_icomp).grid(row = 3, column = 3)
        tk.Entry(frameQ, textvariable = self.q2_jcomp).grid(row = 3, column = 4)
        tk.Entry(frameQ, textvariable = self.q2_kcomp).grid(row = 3, column = 5)

        # Create a frame for the operations
        frameOper = tk.Frame(window)
        frameOper.pack()
        tk.Button(frameOper, text = '+', command = self.addQuaternions).grid(row = 1, column = 1)
        tk.Button(frameOper, text = '-', command = self.subQuaternions).grid(row = 1, column = 2)
        tk.Button(frameOper, text = '*', command = self.mulQuaternions).grid(row = 1, column = 3)
        tk.Button(frameOper, text = '/', command = self.divQuaternions).grid(row = 1, column = 4)

        # Create a frame to show the answer
        frameAnswer = tk.Frame(window)
        frameAnswer.pack()
        tk.Label(frameAnswer, text = "Answer: ").grid(row = 1, column = 1)
        self.answer = tk.StringVar()
        labelAnswer = tk.Label(frameAnswer, textvariable = self.answer).grid(row = 1, column = 2)

        window.mainloop()

    # Get quaternions from the given input. Returns None if an exception occurs
    def getQuaternions(self):
        try:
            q1 = Quaternion(self.q1_rcomp.get(), self.q1_icomp.get(),
                            self.q1_jcomp.get(), self.q1_kcomp.get())
            q2 = Quaternion(self.q2_rcomp.get(), self.q2_icomp.get(),
                            self.q2_jcomp.get(), self.q2_kcomp.get())
            return q1, q2
        # If some entry value is not float, the following exception is raised
        except tk.TclError:
            tk.messagebox.showerror("Error", "You did not provide valid values.")
        except:
            tk.messagebox.showerror("If you see this box", "There is an exception I didn't notice!")

    def addQuaternions(self):
        ans = self.getQuaternions()     # For the sake of readability
        if ans:
            self.answer.set(str(format(ans[0] + ans[1], self.fmt)))

    def subQuaternions(self):
        ans = self.getQuaternions()
        if ans:
            self.answer.set(str(format(ans[0] - ans[1], self.fmt)))

    def mulQuaternions(self):
        ans = self.getQuaternions()
        if ans:
            self.answer.set(str(format(ans[0] * ans[1], self.fmt)))

    def divQuaternions(self):
        ans = self.getQuaternions()
        if ans:
            try:
                self.answer.set(str(format(ans[0] / ans[1], self.fmt)))
            except ZeroDivisionError:
                tk.messagebox.showerror("Error", "Can't divide by zero!")

QuaternionGUI()
