import board
import sumTraversal
import logging
from collections import deque

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='65536.log',  
    filemode='w'  
)

# set up a dictionary with key=block number, and value=list of block permutations
# up 
def SixteenBit2List(num):
    return [int(i) for i in bin(num)[2:].zfill(16)]

qUp = dict()
with open ('qLegal/up.txt', 'r') as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]
for line in lines:
    tempSplit = line.split()
    tempKey = int(tempSplit[1])
    if(tempKey in qUp):
        qUp[tempKey].append(SixteenBit2List(int(tempSplit[0])))
    else:
        qUp[tempKey] = []
        qUp[tempKey].append(SixteenBit2List(int(tempSplit[0])))

qDown = dict()
with open ('qLegal/down.txt', 'r') as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]
for line in lines:
    tempSplit = line.split()
    tempKey = int(tempSplit[1])
    if(tempKey in qDown):
        qDown[tempKey].append(SixteenBit2List(int(tempSplit[0])))
    else:
        qDown[tempKey] = []
        qDown[tempKey].append(SixteenBit2List(int(tempSplit[0])))
        
qLeft = dict()
with open ('qLegal/left.txt', 'r') as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]
for line in lines:
    tempSplit = line.split()
    tempKey = int(tempSplit[1])
    if(tempKey in qLeft):
        qLeft[tempKey].append(SixteenBit2List(int(tempSplit[0])))
    else:
        qLeft[tempKey] = []
        qLeft[tempKey].append(SixteenBit2List(int(tempSplit[0])))

qRight = dict()
with open ('qLegal/right.txt', 'r') as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]
for line in lines:
    tempSplit = line.split()
    tempKey = int(tempSplit[1])
    if(tempKey in qRight):
        qRight[tempKey].append(SixteenBit2List(int(tempSplit[0])))
    else:
        qRight[tempKey] = []
        qRight[tempKey].append(SixteenBit2List(int(tempSplit[0])))
        


def traversal989694():
    # traversal sum permutation for 98

    # define a class for BFS
    class bfsProcess:
        def __init__(self, candidateSeq, currentCandidateNumLeft, nextIndexToFill, listPositionsToFill, listBoard):
            self.candidateSeq = candidateSeq[:] # the first to traversal stands on the right
            self.currentCandidateNumLeft = currentCandidateNumLeft[:]
            self.nextIndexToFill = nextIndexToFill
            self.listPositionsToFill = listPositionsToFill[:]
            self.board = listBoard[:]
            self.listCanFillIndex = []
            i = len(listPositionsToFill) - 1
            tempSpaceCounted = 0
            while(i>=nextIndexToFill and i>0):
                if(listBoard[listPositionsToFill[i]] == 0):
                    tempSpaceCounted += 1
                    if(tempSpaceCounted >= currentCandidateNumLeft[-1]):
                        self.listCanFillIndex.append(listPositionsToFill[i])
                i -= 1
                
            
        def goForward(self):
            result = []
            for tempIndex in self.listCanFillIndex:
                tempBoard = self.board[:]
                tempBoard[tempIndex] = self.candidateSeq[-1]
                # modify candidateSeq and currentCandidateNumLeft
                tempCurrentCandidateNumLeft = self.currentCandidateNumLeft[:]
                tempCurrentCandidateNumLeft[-1] -= 1
                if tempCurrentCandidateNumLeft[-1] == 0:
                    tempCurrentCandidateNumLeft.pop()
                    tempCandidateSeq = self.candidateSeq[:-1]
                else:
                    tempCandidateSeq = self.candidateSeq[:]
                # modify nextIndexToFill
                tempNextIndexToFill = tempIndex+1
                tempListPositionsToFill = self.listPositionsToFill[:]
                result.append(bfsProcess(tempCandidateSeq,tempCurrentCandidateNumLeft,tempNextIndexToFill,tempListPositionsToFill,tempBoard))
                
            # return a list
            pass
    
    # test with a small case
    
        

if (__name__ == "__main__"):
    traversal989694()