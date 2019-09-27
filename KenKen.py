import sys
import time
import array
import random
from HelperFunctions import *
from Node import Node

simpleIterations = 0
bestIterations = 0
localIterations = 0

#Simple backtracking search algorithm
def simpleSolve(puzzle, dictionary, solution, signDict, answerDict):
    global simpleIterations
    nodeSolution = [[Node(0,len(puzzle)) for i in range(0, len(solution))] for j in range(0,len(solution))]
    currentNode = Node(0,0)
    currentRow = 0
    currentCol = 0
    while True:
        #Check if current solution isValid and filled out
        if(isValid(puzzle, dictionary, nodeToSolution(nodeSolution), signDict, answerDict) and solutionFilled(nodeToSolution(nodeSolution))):
            return True, nodeToSolution(nodeSolution)

        #Check if backtracking failed
        if(currentRow == -1 or currentCol == -1):
            return False, "No Solution Found"

        currentNode = nodeSolution[currentRow][currentCol]

        #Trys the next value
        currentNode.current+=1
        simpleIterations+=1

        #If it is maxed out, backtrack. If so, it sets current to 0 and goes back
        if(currentNode.current > currentNode.max):
            currentNode.current = 0
            (row,col) = previousNode(currentRow, currentCol, nodeSolution)
            currentRow = row
            currentCol = col
            continue

        #Checks to see if the next value is valid. If so, it goes to the next node
        if(isValid(puzzle, dictionary, nodeToSolution(nodeSolution), signDict, answerDict)):
            (row,col) = nextNode(currentRow, currentCol, nodeSolution)
            currentRow = row
            currentCol = col
            continue

        #Otherwise backtracks to previous node
        else:
            if(currentNode.current == currentNode.max):
                currentNode.current = 0
                (row,col) = previousNode(currentRow, currentCol, nodeSolution)
                currentRow = row
                currentCol = col
    return False, "No Solution Found"


#Best backtracking search algorithm (using domain filtering)
def bestSolve(puzzle, dictionary, solution, signDict, answerDict):
    global bestIterations
    nodeSolution = [[Node(0,len(puzzle)) for i in range(0, len(solution))] for j in range(0,len(solution))]
    currentNode = Node(0,0)
    currentRow = 0
    currentCol = 0
    while True:
        #Check if current solution isValid and filled out (no zeroes)
        if(isValid(puzzle, dictionary, nodeToSolution(nodeSolution), signDict, answerDict) and solutionFilled(nodeToSolution(nodeSolution))):
            return True, nodeToSolution(nodeSolution)

        #Check if backtracking failed
        if(currentRow == -1 or currentCol == -1):
            return False, "No Solution Found"

        currentNode = nodeSolution[currentRow][currentCol]

        #Trys the next value if it is not already in the domain
        if(currentNode.current+1 in getDomain(currentRow, currentCol, nodeSolution)):
            currentNode.current+=1
            continue
        currentNode.current+=1
        bestIterations+=1

        #If it is maxed out, backtrack
        if(currentNode.current > currentNode.max):
            currentNode.current = 0
            (row,col) = previousNode(currentRow, currentCol, nodeSolution)
            currentRow = row
            currentCol = col
            continue

        #Checks to see if the value is valid to the puzzle
        if(isValid(puzzle, dictionary, nodeToSolution(nodeSolution), signDict, answerDict)):
            (row,col) = nextNode(currentRow, currentCol, nodeSolution)
            currentRow = row
            currentCol = col
            continue

        #Otherwise backtracks to previous node and sets the current to 0
        else:
            if(currentNode.current == currentNode.max):
                currentNode.current = 0
                (row,col) = previousNode(currentRow, currentCol, nodeSolution)
                currentRow = row
                currentCol = col
    return False, "No Solution Found"

#Local Search algorithm (using hill climbing)
def localSolve(puzzle, dictionary, solution, signDict, answerDict):
    global localIterations
    #Creates an initial, random solution
    startSolution = startPuzzle(solution)
    currentSolution = startSolution.copy()
    currentPoints = 0
    if(isValid(puzzle, dictionary, currentSolution, signDict, answerDict)):
        return True, currentSolution
    
    #Iterates through until it reaches a termination maximum
    while localIterations < 250000:
        #Selects a random row and column
        testSolution = currentSolution.copy()
        randomRow = random.randint(0,len(solution)-1)
        randomCol = random.randint(0, len(solution)-1)

        #Swap random choice with another value in that row
        swapRow = randomRow
        swapCol = random.randint(0,len(solution)-1)
        temp = testSolution[randomRow][randomCol]
        testSolution[randomRow][randomCol] = testSolution[swapRow][swapCol]
        testSolution[swapRow][swapCol] = temp
        localIterations+=1

        #Checks if it is valid
        if(isValid(puzzle, dictionary, testSolution, signDict, answerDict) and solutionFilled(testSolution)):
            return True, testSolution
        #Compares the points from the test solution to the current solution's points and if it is higher,
        #the current solution becomes the test solution and current points becomes the points of the new solution.
        if(getPoints(puzzle, dictionary, testSolution, signDict, answerDict) > currentPoints):
            currentSolution = testSolution
            currentPoints = getPoints(puzzle, dictionary, currentSolution, signDict, answerDict)
    return False, "Maximum"




#Setup
file = openFile('puzzle4.txt')
puzzle = createPuzzle(file)
dictionary = createDict(file)
solution = [[0 for i in range(0, len(puzzle))] for j in range(0,len(puzzle))]
signDict = createSignDict(dictionary)
ansDict = createAnswerDict(dictionary)

#Output
simpleSolution = simpleSolve(puzzle, dictionary, solution, signDict, ansDict)
bestSolution = bestSolve(puzzle, dictionary, solution, signDict, ansDict)
print(" ")
printPuzzles(bestSolution[1])
print(" ")
print("Simple Iterations:", simpleIterations)
print("Best Iterations:", bestIterations)
localSolution = localSolve(puzzle, dictionary, solution, signDict, ansDict)
if(localSolution[0]):
    print("Local Iterations:", localIterations)
else:
    print("Local Iterations: Max")
