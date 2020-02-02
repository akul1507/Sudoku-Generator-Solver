import random
import time as t
from tkinter import *
from copy import deepcopy
from tkinter import messagebox


class SudokuFrame(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.pack(fill=BOTH)
        self.data = []
        self.square = []

        # Divide the Sudoku in 9 sub grids

        for i in range(3):
            for j in range(3):
                x = Frame(self, bd=2, bg='black')
                self.square.append(x)
                x.grid(row=i, column=j)

        for i in range(9):
            line = []
            for j in range(9):
                # Put each sub-square in the correct square
                if i <= 2 and j <= 2:
                    square = self.square[0]
                elif i <= 2 and 2 < j <= 5:
                    square = self.square[1]
                elif i <= 2 and j > 5:
                    square = self.square[2]
                elif 2 < i <= 5 and j <= 2:
                    square = self.square[3]
                elif 2 < i <= 5 and 2 < j <= 5:
                    square = self.square[4]
                elif 2 < i <= 5 and j > 5:
                    square = self.square[5]
                elif i > 5 and j <= 2:
                    square = self.square[6]
                elif i > 5 and 2 < j <= 5:
                    square = self.square[7]
                elif i > 5 and j > 5:
                    square = self.square[8]

                cell = Entry(square, width=2, justify=CENTER, font='arial 24')
                line.append(cell)
                cell.grid(row=i, column=j)
            self.data.append(line)


class Sudoku:
    # variables:
    root = Tk()

    def __init__(self):
        # set title
        self.root.title('Sudoku Solver')

        # Disable resizing of the frame
        self.root.resizable(width=False, height=False)
        self.board = SudokuFrame(self.root)
        self.clearButton = Button(self.root, text='Clear', font='arial 10 bold', command=self.clear)
        self.clearButton.pack(side=RIGHT)
        S=[[0 for _ in range(9)] for _ in range(9)]
        self.solveButton = Button(self.root, text='Solve', font='arial 10 bold', command= lambda: self.solve(S))
        self.solveButton.pack(side=RIGHT)
        self.generateButton = Button(self.root, text='Random Game ', font='arial 10 bold', command=lambda: self.generate(S))
        self.generateButton.pack(side=RIGHT)

        self.text = StringVar()
        self.label = Label(self.root, textvariable=self.text, font='arial 12')
        self.label.pack(side=LEFT)

    def run(self):
        self.root.mainloop()

    # Functions to check if a number can be placed in a row, column or sub grid

    def isempty(self,S, pos):
        for i in range(9):
            for j in range(9):
                if S[i][j] == 0:
                    pos[0] = i
                    pos[1] = j
                    return True
        return False

    def checkrow(self,S, row, num):
        for i in range(9):
            if S[row][i] == num:
                return False
        return True

    def checkcol(self,S, col, num):
        for i in range(9):
            if S[i][col] == num:
                return False
        return True

    def checkbox(self,S, row, col, num):
        for i in range(row, row + 3):
            for j in range(col, col + 3):
                if S[i][j] == num:
                    return False
        return True

    def issafe(self,S, x, y, num):
        return self.checkrow(S,x, num) and self.checkcol(S,y, num) and self.checkbox(S,x - x % 3, y - y % 3, num)

    def backtrack(self,S):
        pos = [0, 0]
        if not self.isempty(S,pos):
            return True

        x = pos[0]
        y = pos[1]

        for i in range(1, 10):
            if self.issafe(S,x, y, i):
                S[x][y] = i

                if self.backtrack(S):
                    return True

                S[x][y] = 0

        return False

    # Function to clear the grid interface
    def clear(self):
        for i in range(9):
            for j in range(9):
                self.board.data[i][j].delete(0, 'end')
                self.board.data[i][j].configure(fg='black')
                self.board.data[i][j].configure(bg='white')
        self.text.set("")

    # Function to find empty cell

    def solve(self,S):
        validBoard = True
        solvable = True

        for i in range(9):
            for j in range(9):
                self.board.data[i][j].configure(bg='white')
                if self.board.data[i][j].get() in set("123456789"):
                    S[i][j] = int(self.board.data[i][j].get())
                elif self.board.data[i][j].get() == '':
                    S[i][j] = 0
                else:
                    if validBoard:
                        validBoard = False
                    self.board.data[i][j].configure(bg='yellow')

        for i in range(9):
            for j in range(9):
                num = S[i][j]
                S[i][j]=0
                if num and not self.issafe(S,i, j, num):
                    solvable = False
                    self.board.data[i][j].configure(bg='red')
                S[i][j] = num

        if not solvable:
            messagebox.showinfo('Error', 'The game has no solution.')

        if not validBoard:
            messagebox.showinfo("Error", "Enter a valid digit between 1 and 9.")

        if validBoard and solvable:
            # Solve the sudoku
            time1 = t.process_time()
            self.backtrack(S)
            time2 = t.process_time()

            # Convert back the 2D list to display it on the interface
            for i in range(9):
                for j in range(9):
                    if self.board.data[i][j].get() == '':
                        self.board.data[i][j].delete(0)
                        # Write calculated digits in green
                        self.board.data[i][j].configure(fg='#0B0')
                        self.board.data[i][j].insert(0, str(S[i][j]))

            # Display the time taken to solve the grid
            dispText = "Resolved in " + str(round(time2 - time1, 2)) + " s"
            self.text.set(dispText)

    def generate(self, S):
        S = [[0 for _ in range(9)] for _ in range(9)]
        self.clear()
        missing_number = 50
        for k in range(0, 9, 3):
            for i in range(k, k + 3):
                for j in range(k, k + 3):
                    num = random.randint(1, 9)

                    while not self.checkbox(S,k, k, num):
                        num = random.randint(1, 9)

                    S[i][j] = num

        self.backtrack(S)

        while missing_number > 0:
            x = random.randint(0, 8)
            y = random.randint(0, 8)

            if S[x][y] != 0:
                S[x][y] = 0
                missing_number -= 1

        for i in range(9):
            for j in range(9):
                if self.board.data[i][j].get() == '':
                    self.board.data[i][j].delete(0)
                    # Write calculated digits in green
                    self.board.data[i][j].configure(fg='blue')
                    if S[i][j] != 0:
                        self.board.data[i][j].insert(0, str(S[i][j]))
                    else:
                        self.board.data[i][j].insert(0, "")
        return

if __name__ == '__main__':
    sudokuGame = Sudoku()
    sudokuGame.run()
