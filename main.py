"""
Automated Sudoku Puzzle Solver
Created by Evelyn Kammerzell
Based on "Good Sudoku" app on Apple Arcade
Uses .csv files with sudoku puzzles inputted row by row with each cell separated by a comma
"""

import csv as c
from cell_class import *

# base build of dictionaries for puzzle sections
master = {}
columns = {"1": [], "2": [], "3": [], "4": [], "5": [], "6": [], "7": [], "8": [], "9": []}
rows = {"1": [], "2": [], "3": [], "4": [], "5": [], "6": [], "7": [], "8": [], "9": []}
houses = {"1": [], "2": [], "3": [], "4": [], "5": [], "6": [], "7": [], "8": [], "9": []}
cleared = []
views = (rows, columns, houses)


# function to fill dictionaries
def build(puzzle_file):
    try:
        file = open(puzzle_file, "r")
    except FileNotFoundError:
        print("Puzzle not found!")
        exit()
    puzzle = c.reader(file)

    col = "1"
    ro = "1"
    hou = "1"

    for line in puzzle:
        for num in line:
            ref = col + ro + hou
            master[ref] = cells(col, ro, hou, ref, num.strip())
            columns[col].append(master[ref])
            rows[ro].append(master[ref])
            houses[hou].append(master[ref])
            if num.strip() != "0":
                master.pop(ref)

            col = str(int(col) + 1)
            hou = check_house(col, ro)
        ro = str(int(ro) + 1)
        col = "1"
        hou = check_house(col, ro)


# routine function to update puzzle if a cell is solved
def cell_check(cell):
    cont = False
    if cell.solved:
        return "s"
    control = list(cell.possible)
    single_views = (cell.row, cell.column, cell.house)
    for z, iter2 in zip(views, single_views):
        for y in z[iter2]:
            if cell.reference != y.reference and y.solved:
                val = y.value
                cell.check(val)
                if cell.solved:
                    cell_update(cell)
    if len(control) > len(cell.possible):
        cont = True
    return cont


# pattern detection function 1
def hidden_single():
    num = 1
    cell = []
    while num < 10:
        for z in views:
            for iter4 in z:
                for y in z[iter4]:
                    if str(num) in y.possible:
                        cell.append(y)
                        if len(cell) > 1:
                            cell = []
                            break
                if len(cell) == 1:
                    cell[0].possible = [str(num)]
                    cell[0].solve()
                    cell_update(cell[0])
            cell = []
        num += 1


# pattern detection function 2
def naked_pair(cell):
    test = cell.possible
    single_views = (cell.row, cell.column, cell.house)
    for z, k in zip(views, single_views):
        for iter5 in z[k]:
            if not iter5.solved and cell.reference != iter5.reference:
                if len(iter5.possible) == 2 and iter5.possible == test:
                    one = test[0]
                    two = test[1]
                    for y in z[k]:
                        if cell.reference != y.reference and iter5.reference != y.reference:
                            y.check(one)
                            y.check(two)
                            if y.solved:
                                cell_update(y)


# pattern detection function 3
def locked_candidate():
    for k in (rows, columns):
        for iter6 in k:
            for y in k[iter6]:
                if not y.solved:
                    for z in y.possible:
                        balance = False
                        for a in k[iter6]:
                            if y.house != a.house and z in a.possible:
                                balance = True
                                break
                        if not balance:
                            for b in houses[y.house]:
                                if not b.solved:
                                    if k == rows:
                                        if b.row != y.row:
                                            b.check(z)
                                    elif k == columns:
                                        if b.column != y.column:
                                            b.check(z)
                                    if b.solved:
                                        cell_update(b)
                                        solve1()


# pattern detection function 4
def pointing_tuple():
    num = 1
    while num < 10:
        for iter1 in houses:
            r = []
            col1 = []
            for y in houses[iter1]:
                if str(num) in y.possible:
                    r.append(y.row)
                    col1.append(y.column)
            if len(r) > 1 and len(set(r)) == 1:
                for k in rows[r[0]]:
                    if k.house != iter1:
                        k.check(str(num))
                        if k.solved:
                            cell_update(k)
                            solve1()
            if len(col1) > 1 and len(set(col1)) == 1:
                for k in columns[col1[0]]:
                    if k.house != iter1:
                        k.check(str(num))
                        if k.solved:
                            cell_update(k)
                            solve1()
        num += 1


# updates cells as new information is found
def cell_update(cell):
    single_views = (cell.row, cell.column, cell.house)
    for iter7, y in zip(views, single_views):
        for z in iter7[y]:
            if z.reference != cell.reference:
                z.check(cell.value)


# printing board
def show_board():
    line = ""
    col = 1
    row = 1
    for iter8 in rows:
        for y in rows[iter8]:
            line += y.value
            line += " "
            if col != 9:
                if col == 3 or col == 6:
                    line += "| "
                col += 1
            else:
                print(line)
                line = ""
                if row == 3 or row == 6:
                    print("---------------------")
                row += 1
                col = 1
    print()


# starting function to check for naked and hidden singles
def solve1():
    check = False
    while not check:
        check = True
        for iter9 in master:
            con = cell_check(master[iter9])
            if con == 's':
                cleared.append(iter9)
            elif con:
                check = False
                if master[iter9].solved:
                    cleared.append(iter9)
        if len(cleared) > 0:
            for iter9 in cleared:
                master.pop(iter9)
        cleared.clear()


# secondary function looking for naked pairs
def solve2():
    for iter10 in master:
        if len(master[iter10].possible) > 2:
            continue
        naked_pair(master[iter10])


# control function
def main():
    base_puzzle = input("Please enter the name of the .csv file: ")
    if base_puzzle[-3:] != ".csv":
        base_puzzle += ".csv"
    build(base_puzzle)
    print("Starting board: \n")
    show_board()
    cycle = True
    while cycle:
        hold = len(master)
        solvers = (solve1, solve2, solve1, hidden_single, locked_candidate, pointing_tuple, solve1)
        for x in solvers:
            x()
        if hold == len(master) or len(master) == 0:
            cycle = False

    print("Board after automated solving: ")
    show_board()


main()
