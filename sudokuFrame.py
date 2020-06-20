from tkinter import *

class sudokuFrame(Frame):
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