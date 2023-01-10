"""
Automated Sudoku Puzzle Solver
Created by Evelyn Kammerzell
Based on "Good Sudoku" app on Apple Arcade
Uses .csv files with sudoku puzzles inputted row by row with each cell separated by a comma
"""


# base class to define each of the 81 cells on a sudoku board
class cells:
    def __init__(self, column, row, house, reference, value):
        self.column = column
        self.row = row
        self.house = house
        self.reference = reference
        self.value = value
        self.solved = False
        if value != "0":
            self.solved = True
        self.possible = []
        if not self.solved:
            self.possible = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    def solve(self):
        if len(self.possible) == 1:
            self.value = self.possible[0]
            self.solved = True
            self.possible = tuple(self.possible)

    def check(self, value):
        if value in self.possible:
            self.possible.remove(value)
        self.solve()


# sorting function used during initial board building to determine cell's house
def check_house(column, row):
    if column in "123":
        if row in "123":
            return "1"
        elif row in "456":
            return "4"
        else:
            return "7"
    elif column in "456":
        if row in "123":
            return "2"
        elif row in "456":
            return "5"
        else:
            return "8"
    else:
        if row in "123":
            return "3"
        elif row in "456":
            return "6"
        else:
            return "9"
