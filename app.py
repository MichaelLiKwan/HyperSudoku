import copy, heapq, sys

def readInput(filename):
    f = open(filename, "r")
    lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip().split(" ")
    f.close()
    return lines

def forwardCheck(puzzle, domains):
    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            if puzzle[row][col] != "0":
                val = puzzle[row][col]
                # check row and col contraints
                for i in range(9):
                    try:
                        domains[row][i].remove(val)
                    except ValueError:
                        pass
                for i in range(9):
                    try:
                        domains[i][col].remove(val)
                    except ValueError:
                        pass

                # check nonoverlapping region constraints
                if (0 <= row < 3) and (0 <= col < 3):
                    for i in range(0,3):
                        for j in range(0,3):
                            try:
                                domains[i][j].remove(val)
                            except ValueError:
                                pass
                elif (0 <= row < 3) and (3 <= col < 6):
                    for i in range(0,3):
                        for j in range(3,6):
                            try:
                                domains[i][j].remove(val)
                            except ValueError:
                                pass
                elif (0 <= row < 3) and (6 <= col < 9):
                    for i in range(0,3):
                        for j in range(6,9):
                            try:
                                domains[i][j].remove(val)
                            except ValueError:
                                pass
                elif (3 <= row < 6) and (0 <= col < 3):
                    for i in range(3,6):
                        for j in range(0,3):
                            try:
                                domains[i][j].remove(val)
                            except ValueError:
                                pass
                elif (3 <= row < 6) and (3 <= col < 6):
                    for i in range(3,6):
                        for j in range(3,6):
                            try:
                                domains[i][j].remove(val)
                            except ValueError:
                                pass
                elif (3 <= row < 6) and (6 <= col < 9):
                    for i in range(3,6):
                        for j in range(6,9):
                            try:
                                domains[i][j].remove(val)
                            except ValueError:
                                pass
                elif (6 <= row < 9) and (0 <= col < 3):
                    for i in range(6,9):
                        for j in range(0,3):
                            try:
                                domains[i][j].remove(val)
                            except ValueError:
                                pass
                elif (6 <= row < 9) and (3 <= col < 6):
                    for i in range(6,9):
                        for j in range(3,6):
                            try:
                                domains[i][j].remove(val)
                            except ValueError:
                                pass
                elif (6 <= row < 9) and (6 <= col < 9):
                    for i in range(6,9):
                        for j in range(6,9):
                            try:
                                domains[i][j].remove(val)
                            except ValueError:
                                pass

                # check overlapping constraints
                if (1 <= row < 4) and (1 <= col < 4):
                    for i in range(1,4):
                        for j in range(1,4):
                            try:
                                domains[i][j].remove(val)
                            except ValueError:
                                pass
                elif (1 <= row < 4) and (5 <= col < 8):
                    for i in range(1,4):
                        for j in range(5,8):
                            try:
                                domains[i][j].remove(val)
                            except ValueError:
                                pass
                elif (5 <= row < 8) and (1 <= col < 4):
                    for i in range(5,8):
                        for j in range(1,4):
                            try:
                                domains[i][j].remove(val)
                            except ValueError:
                                pass
                elif (5 <= row < 8) and (5 <= col < 8):
                    for i in range(5,8):
                        for j in range(5,8):
                            try:
                                domains[i][j].remove(val)
                            except ValueError:
                                pass

    #change domains for variables that are already assigned
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != "0":
                domains[i][j] = [puzzle[i][j]]

    # make sure all domains are not empty
    solution = True
    for i in range(9):
        for j in range(9):
            if len(domains[i][j]) == 0:
                solution = False

    return puzzle, domains, solution

def selectUnassignedVar(puzzle, domains):
    # MRV
    minRem = len(domains[0][0])
    minRemVars = []
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == "0":
                newVal = len(domains[i][j])
                if newVal == minRem:
                    minRemVars.append((i,j))
                elif newVal < minRem:
                    minRemVars = []
                    minRem = newVal
                    minRemVars.append((i,j))
                    
    # Degree
    minDeg = None
    varRow = None
    varCol = None
    for elem in minRemVars:
        row, col = elem[0], elem[1]
        deg = 0

        for i in range(9):
            for j in range(9):
                if puzzle[i][j] == "0":
                    if i == row:
                        deg+=1
                    elif j == col:
                        deg+=1
                    elif (0 <= row < 3) and (0 <= col < 3):
                        if (0 <= i < 3) and (0 <= j < 3):
                            deg+=1
                    elif (0 <= row < 3) and (3 <= col < 6):
                        if (0 <= i < 3) and (3 <= j < 6):
                            deg+=1
                    elif (0 <= row < 3) and (6 <= col < 9):
                        if (0 <= i < 3) and (6 <= j < 9):
                            deg+=1
                    elif (3 <= row < 6) and (0 <= col < 3):
                        if (3 <= i < 6) and (0 <= j < 3):
                            deg+=1
                    elif (3 <= row < 6) and (3 <= col < 6):
                        if (3 <= i < 6) and (3 <= j < 6):
                            deg+=1
                    elif (3 <= row < 6) and (6 <= col < 9):
                        if (3 <= i < 6) and (6 <= j < 9):
                            deg+=1
                    elif (6 <= row < 9) and (0 <= col < 3):
                        if (6 <= i < 9) and (0 <= j < 3):
                            deg+=1
                    elif (6 <= row < 9) and (3 <= col < 6):
                        if (6 <= i < 9) and (3 <= j < 6):
                            deg+=1
                    elif (6 <= row < 9) and (6 <= col < 9):
                        if (6 <= i < 9) and (6 <= j < 9):
                            deg+=1
                    elif (1 <= row < 4) and (1 <= col < 4):
                        if (1 <= i < 4) and (1 <= j < 4):
                            deg+=1
                    elif (1 <= row < 4) and (5 <= col < 8):
                        if (1 <= i < 4) and (5 <= j < 8):
                            deg+=1
                    elif (5 <= row < 8) and (1 <= col < 4):
                        if (5 <= i < 8) and (1 <= j < 4):
                            deg+=1
                    elif (5 <= row < 8) and (5 <= col < 8):
                        if (5 <= i < 8) and (5 <= j < 8):
                            deg+=1

        if minDeg == None:
            minDeg = deg
            varRow = row
            varCol = col

        if deg < minDeg:
            minDeg = deg
            varRow = row
            varCol = col

    return varRow, varCol

def main():
    #filename = input("What is the input filename?")
    puzzle = readInput("input1.txt")
    domains = []
    for i in range(9):
        newList = []
        for j in range(9):
            newList.append(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        domains.append(newList)
    puzzle, domains, solution = forwardCheck(puzzle, domains)

    if not solution:
        # No solution
        pass

    for elem in domains:
        print(elem, end='\n')

    print(selectUnassignedVar(puzzle, domains))


main()