import sys
import time
import array
import random
from random import shuffle
from Node import Node

#Opens the .txt puzzle file and returns an array with the puzzle data
def openFile(string):
    puzzle = []
    with open(string) as f:
        lines = f.readlines()
    for line in lines:
        puzzle.append(line.strip().split('\t'))
    return puzzle

#Modifies the file and creates a 2d array with the letters of the puzzle
def createPuzzle(array):
    arr = []
    length = int(array[0][0])
    i = 1
    while(i < length + 1):
        arr.append(array[i][0])
        i+=1
    return arr

#Creates a dictionary with the number and sign for each letter value
def createDict(array):
    dict = {}
    length = int(array[0][0])
    i = length + 1
    while(i < len(array)):
        letter = array[i][0][0]
        value = array[i][0][2:len(array[i][0])]
        dict[letter] = value
        i+=1
    return dict

#Checks the validity of the puzzle in terms of values/math
def checkMath(puzzle, dictionary, solution, signDict, answerDict):
    valDict = createValuesDict(puzzle, dictionary, solution)

    #Removes equations/blocks that are not done
    valuesDict = {}
    for key in valDict:
        if not 0 in valDict[key]:
            valuesDict[key] = valDict[key]
    
    #Runs through each block/array in the values dict and evaluates the equation
    for key in valuesDict:
        equation = ''
        i = 0
        for value in valuesDict[key]:
            i+=1
            if(i != len(valuesDict[key])):
                equation = equation + str(value) + signDict[key]
            else:
                equation = equation + str(value)
        if( (eval(equation) != answerDict[key]) and (eval(equation[::-1]) != answerDict[key]) ):
            return False
    return True

#Checks the validity of the puzzle in terms of row and column validity
def checkRowCol(solution):          
    for row in solution:
        if(sorted(list(set(row))) != sorted(row)):
            return False
    cols = []
    for col in range(len(solution)):
        for row in solution:
            cols += [row[col]]
        if(sorted(list(set(cols))) != sorted(cols)):
            return False
        cols = []
    return True

#Creates a dictionary that contains the operation sign for each cage
def createSignDict(dictionary):
    signDict = {}
    for key in dictionary:
        if("+" in dictionary[key] or "-" in dictionary[key] or "*" in dictionary[key] or "/" in dictionary[key]):
            signDict[key] = dictionary[key][len(dictionary[key]) - 1]
        else:
            signDict[key] = ''
    return signDict

#Creates a dictionary that contains the correct answer for each cage
def createAnswerDict(dictionary):
    answerDict = {}
    for key in dictionary:
        string = ''
        for letter in dictionary[key]:
            if letter.isdigit():
                string+=letter
        answerDict[key] = int(string)
    return answerDict

#Creates a dictionary that contains letters as the key and current values for that cage as the value (list)
def createValuesDict(puzzle, dictionary, solution):
    valuesDict = {}
    for key in dictionary:
        valuesDict[key] = []
    row = 0
    for string in puzzle:
        col = 0
        for letter in string:
            valuesDict[letter].append(solution[row][col])
            col+=1
        row+=1
    return valuesDict

#Checks to see if a given solution is filled out (no zeroes)
def solutionFilled(solution):
    for row in range(0, len(solution)):
        for col in range(0, len(solution[0])):
            if(solution[row][col] == 0):
                return False
    return True

#Checks if a list has duplicates (ignores 0s)
def isDistinct(list):
    used = []
    for i in list:
        if i == 0:
            continue
        if i in used:
            return False
        used.append(i)
    return True

#Checks if the solution is valid. Returns false if math or row/col constraints are not satisfied (ignores cases with 0s)
def isValid(puzzle, dictionary, solution, signDict, answerDict):
    for row in range(0, len(solution)):
        if not isDistinct(solution[row]):
            return False

    col = [[0 for i in range(0, len(solution))] for j in range(0,len(solution))]
    for row in range(0, len(solution)):
        for i in range(0,len(solution[row])):
            col[row][i] = solution[i][row]
    
    for column in range(0, len(col)):
        if not isDistinct(col[column]):
            return False

    if not checkMath(puzzle, dictionary, solution, signDict, answerDict):
        return False
    return True

#Converts the node 2d array to a 2d array of the nodes current values (numbers)
def nodeToSolution(nodeSolution):
    solution = [[0 for i in range(0, len(nodeSolution))] for j in range(0,len(nodeSolution))]
    for row in range(0,len(nodeSolution)):
        for col in range(0, len(nodeSolution[0])):
            solution[row][col] = nodeSolution[row][col].getCurrent()
    return solution

#From the current row, col returns the row, col for the next node if it exists
def nextNode(row, col, nodeSolution):
    if(row == len(nodeSolution) and col == len(nodeSolution)):
        return (-1,-1)
    if(col == len(nodeSolution) - 1):
        return (row+1, 0)
    return (row, col+1)

#From the current row, col returns the row, col for the previous node if it exists
def previousNode(row, col, nodeSolution):
    if(row == 0 and col == 0):
        return (-1,-1)
    if(col == 0):
        return (row-1, len(nodeSolution) - 1)
    return (row, col-1)

#Gets the domain for the current row and col (for detecting already potential conflicitng values)
def getDomain(row, col, nodeSolution):
    solution = nodeToSolution(nodeSolution)
    rowValues = solution[row]
    colValues = []
    for r in range(0, len(nodeSolution)):
        colValues.append(solution[r][col])
    domain = []
    for r in rowValues:
        if(r != 0):
            domain.append(r)
    for c in colValues:
        if(c != 0 and c not in domain):
            domain.append(c)
    return domain

#Prints the solution in a read-friendly way
def printPuzzles(simple):
    for row in simple:
        for col in row:
            print(col, end='')
        print()


#Gets a starting,random puzzle with no repeats in the rows for the local search
def startPuzzle(solution):
    new = [[0 for i in range(0, len(solution))] for j in range(0,len(solution))]
    for row in range(0,len(solution)):
        for col in range(0,len(solution[0])):
            new[row][col] = (col + 1)
        shuffle(new[row])
    return new

#Calculates and returns total points from math and row,col point values
def getPoints(puzzle, dictionary, solution, signDict, answerDict):
    mathPoints = getMathPoints(puzzle, dictionary, solution, signDict, answerDict)
    rcPoints = getRCPoints(solution)
    return mathPoints + rcPoints

#Calculates a point value for the number of cages/equations have correct numbers
def getMathPoints(puzzle, dictionary, solution, signDict, answerDict):
    points = 0
    valuesDict = createValuesDict(puzzle, dictionary, solution)
    for key in valuesDict:
        equation = ''
        i = 0
        for value in valuesDict[key]:
            i+=1
            if(i != len(valuesDict[key])):
                equation = equation + str(value) + signDict[key]
            else:
                equation = equation + str(value)
        if( (eval(equation) == answerDict[key]) or (eval(equation[::-1]) == answerDict[key]) ):
            points+=1
    return points

#Calculates a point value for the number of row,col values satisfy the constraints
def getRCPoints(solution):
    points = 0
    for row in range(0, len(solution)):
        if isDistinct(solution[row]):
            points+=1

    col = [[0 for i in range(0, len(solution))] for j in range(0,len(solution))]
    for row in range(0, len(solution)):
        for i in range(0,len(solution[row])):
            col[row][i] = solution[i][row]
    
    for column in range(0, len(col)):
        if isDistinct(col[column]):
            points+=1
    return points