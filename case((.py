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
                if(listBoard[i] == 0):
                    tempSpaceCounted += 1
                    if(tempSpaceCounted >= currentCandidateNumLeft[-1]):
                        self.listCanFillIndex.append(listPositionsToFill[i])
                
            
        def goForward(self):
            result = []
            for tempIndex in self.listCanFillIndex:
                tempBoard = self.board[:]
                tempBoard[tempListPositionsToFill[tempIndex]] = self.candidateSeq[-1]
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
                
            # return a list
            pass
    
    dequeSum98 = sumTraversal.traversalFunc(98, 2)
    while(len(dequeSum98) > 0):
        tempSumFormat = dequeSum98.popleft()
        # calculate how many blocks should be used.
        # first calculate the overall sum of the list tempSum
        '''Q
        *CaseType[2]
        !*CaseValue[2]
        !T*TotalPossibilites[2] （等于空位数×10，考虑所有出2和出4的情况）
        {!*Special*SuccessRate[8]}（*Special在特殊情况中是S，普通情况中是N）
        {!p*PCaseType[2]*CaseValue[2]*P[16]*SuccessRate[8]} （未来的P，可重复）
        {!P*PCaseType[2]CaseValue[2]*P[16]} （源自什么样的P可重复）
        '''
        # logging.info("format: "+str(tempSumFormat))
        # Q98
        tempBlocksUsed = sum(tempSumFormat) + 2
        for permutation in qLeft[tempBlocksUsed]:
            
            # list permutation...
            # bfs, place 2 first. No adjacent 2s in each column!
            # check which blocks are used.
            listShouldUseBlock = []
            for i in range(16):
                if(permutation[i] == 1):
                    listShouldUseBlock.append(i)
            # logging.info(listShouldUseBlock)
            pass
        

if (__name__ == "__main__"):
    traversal989694()