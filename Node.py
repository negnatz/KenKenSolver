import sys

class Node:
    def __init__(self, current, max):
        self.current = current
        self.max = max

    def getCurrent(self):
        return self.current
    
    def getMax(self):
        return self.max

    def add(self):
        self.current+=1