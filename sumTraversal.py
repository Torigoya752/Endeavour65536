import numpy as np
import copy
import os
import logging
import board
from collections import deque

class traversal:
    def __init__(self, list_1, remainSum, blockUsed, goForNext, blockAvailMax):
        self.list_1 = list_1[:]
        self.remainSum = remainSum
        self.blockUsed = blockUsed
        self.goForNext = goForNext
        self.blockAvailMax = blockAvailMax

    def BfsTraversal(self):
        if(self.goForNext>=8):
            raise board.Err65536("self.goForNext>=8")
        result = []
        for i in range(16 - self.blockUsed):
            tempNextNumber = 256 >> self.goForNext
            if(self.remainSum - tempNextNumber * i >= 0 and self.blockUsed + i <= self.blockAvailMax):
                tempList_1 = self.list_1[:]
                tempList_1[self.goForNext] = i
                result.append(traversal(tempList_1, self.remainSum - tempNextNumber * i, self.blockUsed + i, self.goForNext + 1, self.blockAvailMax))
        return result
    
def traversalFunc(traversalSum, blockUsed):
    result = deque()
    tempResult = deque()
    tempResult.append(traversal([0] * 8, traversalSum, 0, 0,15-blockUsed))
    while(len(tempResult) > 0):
        tempLeft = tempResult.popleft()
        if(tempLeft.remainSum == 0):
            # logging.info(tempLeft.list_1[:])
            result.append(tempLeft.list_1[:])
        elif(tempLeft.goForNext >= 8):
            # do nothing. Cannot go for next but remain sum is not 0
            pass
        else:
            tempToAppend = tempLeft.BfsTraversal()
            for item in tempToAppend:
                tempResult.append(copy.deepcopy(item))
    return result # deque format
# function traversalFunc
        
        
if(__name__ == "__main__"):
    print(traversalFunc(98,2))