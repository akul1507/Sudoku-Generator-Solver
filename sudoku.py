import random 
import time as t 
from tkinter import * 
from copy import deepcopy
from tkinter import messagebox 
from sudokuFrame import sudokuFrame

class sudoku:
    # variables:
    root = Tk()

    def __init__(self):
        # set title
        self.root.title('Sudoku Solver')

        # Disable resizing of the frame
        self.root.resizable(width=False, height=False)
        self.board = sudokuFrame(self.root)
        self.clearButton = Button(self.root, text='Clear', font='arial 10 bold', command=self.clear)
        self.clearButton.pack(side=RIGHT)
        solutionBoard=[[0 for _ in range(9)] for _ in range(9)]
        S=[[0 for _ in range(9)] for _ in range(9)]
        self.solveButton = Button(self.root, text='Solve', font='arial 10 bold', command= lambda: self.solve(solutionBoard))
        self.solveButton.pack(side=RIGHT)
        self.generateButton = Button(self.root, text='Random Game ', font='arial 10 bold', command=lambda: self.generate(solutionBoard))
        self.generateButton.pack(side=RIGHT)

        self.text = StringVar()
        self.label = Label(self.root, textvariable=self.text, font='arial 12')
        self.label.pack(side=LEFT)

        #Disable the cells initially
        for i in range(9):
            for j in range(9):
                self.board.data[i][j].configure(state=DISABLED)      

    def run(self):
        self.root.mainloop()

    # Functions to check if a number can be placed in a row, column or sub grid

    def isempty(self,solutionBoard, pos):
        for i in range(9):
            for j in range(9):
                if solutionBoard[i][j] == 0:
                    pos[0] = i
                    pos[1] = j
                    return True
        return False

    def checkrow(self,solutionBoard, row, num):
        for i in range(9):
            if solutionBoard[row][i] == num:
                return False
        return True

    def checkcol(self,solutionBoard, col, num):
        for i in range(9):
            if solutionBoard[i][col] == num:
                return False
        return True

    def checkbox(self,solutionBoard, row, col, num):
        for i in range(row, row + 3):
            for j in range(col, col + 3):
                if solutionBoard[i][j] == num:
                    return False
        return True

    def issafe(self,solutionBoard, x, y, num):
        return self.checkrow(solutionBoard,x, num) and self.checkcol(solutionBoard,y, num) and self.checkbox(solutionBoard,x - x % 3, y - y % 3, num)

    def backtrack(self,solutionBoard):
        pos = [0, 0]
        if not self.isempty(solutionBoard,pos):
            return True

        x = pos[0]
        y = pos[1]

        for i in range(1, 10):
            if self.issafe(solutionBoard,x, y, i):
                solutionBoard[x][y] = i

                if self.backtrack(solutionBoard):
                    return True

                solutionBoard[x][y] = 0

        return False

    # Function to clear the grid interface
    def clear(self):
        for i in range(9):
            for j in range(9):
                self.board.data[i][j].config(state=NORMAL)
                self.board.data[i][j].delete(0, 'end')
                self.board.data[i][j].configure(fg='black')
                self.board.data[i][j].configure(bg='white')
        self.text.set("")

    # Function to find empty cell

    def solve(self,solutionBoard):
        validBoard = True
        solvable = True

        for i in range(9):
            for j in range(9):
                self.board.data[i][j].configure(bg='white')
                if self.board.data[i][j].get() in set("123456789"):
                    solutionBoard[i][j] = int(self.board.data[i][j].get())
                elif self.board.data[i][j].get() == '':
                    solutionBoard[i][j] = 0
                else:
                    if validBoard:
                        validBoard = False
                    self.board.data[i][j].configure(bg='yellow')

        for i in range(9):
            for j in range(9):
                num = solutionBoard[i][j]
                solutionBoard[i][j]=0
                if num and not self.issafe(solutionBoard,i, j, num):
                    solvable = False
                    self.board.data[i][j].configure(bg='red')
                solutionBoard[i][j] = num

        if not solvable:
            messagebox.showinfo('Error', 'The game has no solution.')

        if not validBoard:
            messagebox.showinfo("Error", "Enter a valid digit between 1 and 9.")

        if validBoard and solvable:
            # Solve the sudoku
            time1 = t.process_time()
            self.backtrack(solutionBoard)
            time2 = t.process_time()

            # Convert back the 2D list to display it on the interface
            for i in range(9):
                for j in range(9):
                    if self.board.data[i][j].get() == '':
                        self.board.data[i][j].delete(0)
                        # Write calculated digits in green
                        self.board.data[i][j].configure(fg='#0B0')
                        self.board.data[i][j].insert(0, str(solutionBoard[i][j]))

            # Display the time taken to solve the grid
            dispText = "Resolved in " + str(round(time2 - time1, 2)) + " s"
            self.text.set(dispText)

    def generate(self, solutionBoard):
        solutionBoard = [[0 for _ in range(9)] for _ in range(9)]
        self.clear()
        for i in range(9):
            for j in range(9):
                self.board.data[i][j].configure(state=NORMAL)

        missing_number = random.randint(1, 64)
        for k in range(0, 9, 3):
            for i in range(k, k + 3):
                for j in range(k, k + 3):
                    num = random.randint(1, 9)

                    while not self.checkbox(solutionBoard,k, k, num):
                        num = random.randint(1, 9)

                    solutionBoard[i][j] = num

        self.backtrack(solutionBoard)

        while missing_number > 0:
            x = random.randint(0, 8)
            y = random.randint(0, 8)

            if solutionBoard[x][y] != 0:
                solutionBoard[x][y] = 0
                missing_number -= 1

        for i in range(9):
            for j in range(9):
                if self.board.data[i][j].get() == '':
                    self.board.data[i][j].delete(0)
                    # Write calculated digits in green
                    self.board.data[i][j].configure(fg='blue')
                    if solutionBoard[i][j] != 0:
                        self.board.data[i][j].insert(0, str(solutionBoard[i][j]))
                        self.board.data[i][j].configure(state=DISABLED)
                    else:
                        self.board.data[i][j].insert(0, "")
        S=deepcopy(solutionBoard)
        return