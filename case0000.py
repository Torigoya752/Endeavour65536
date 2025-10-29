import board
import sumTraversal
import logging
from collections import deque

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='./case0000.log',  
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
        def __init__(self, candidateSeq, currentCandidateNumLeft, nextIndexToFill, listPositionsToFill, listBanLevel, listBoard):
            self.candidateSeq = candidateSeq[:] # the first to traversal stands on the right
            self.currentCandidateNumLeft = currentCandidateNumLeft[:]
            self.nextIndexToFill = nextIndexToFill
            self.listPositionsToFill = listPositionsToFill[:]
            self.listBanLevel = listBanLevel[:]
            self.board = listBoard[:]
            self.listCanFillIndex = []
            i = len(listPositionsToFill) - 1
            tempSpaceCounted = 0
            while(i>=nextIndexToFill and i>=0):
                if(listBoard[listPositionsToFill[i]] == 0):
                    tempSpaceCounted += 1
                    if(tempSpaceCounted >= currentCandidateNumLeft[-1]):
                        self.listCanFillIndex.append(i)
                i -= 1
                
            
        def goForward(self):
            result = []
            for tempIndex in self.listCanFillIndex:
                tempBoard = self.board[:]
                tempBoard[self.listPositionsToFill[tempIndex]] = self.candidateSeq[-1]
                # modify candidateSeq and currentCandidateNumLeft
                tempCurrentCandidateNumLeft = self.currentCandidateNumLeft[:]
                tempCurrentCandidateNumLeft[-1] -= 1
                if tempCurrentCandidateNumLeft[-1] == 0:
                    tempCurrentCandidateNumLeft.pop()
                    tempCandidateSeq = self.candidateSeq[:-1]
                    tempNextIndexToFill = 0
                else:
                    tempCandidateSeq = self.candidateSeq[:]
                    # tempNextIndexToFill = tempIndex+1
                    # TODO tempIndex+2 when the element in listBanLevel is active, +1 when inactive
                    # Look at listBanLevel[tempIndex+1]. If nextIndexToFill[-1] is 1 and level>=1, active
                    # If level is 2 and listBoard[tempIndex-1] and listBoard[tempIndex] and the number to fill are all same, active
                    # If level is 3, active
                    if(tempCandidateSeq[-1]==1 and self.listBanLevel[tempIndex+1]>=1):
                        tempNextIndexToFill = tempIndex+2
                    elif(self.listBanLevel[tempIndex+1]==2 and tempBoard[self.listPositionsToFill[tempIndex]-1]==tempBoard[self.listPositionsToFill[tempIndex]] ):
                        tempNextIndexToFill = tempIndex+2
                    elif(self.listBanLevel[tempIndex+1]==3):
                        tempNextIndexToFill = tempIndex+2
                    else:
                        tempNextIndexToFill = tempIndex+1
                
                result.append(bfsProcess(tempCandidateSeq,tempCurrentCandidateNumLeft,tempNextIndexToFill,self.listPositionsToFill[:],self.listBanLevel[:],tempBoard))
                
            # return a list
            return result
    
    # test with a small case
    exampleProcess = bfsProcess([4,2,1],[5,2,5],0,[0,1,2,3,4,5,6,7,8,9,10,12,13,14],[0,3,3,3,0,0,3,3,0,0,2,0,1,2],[0,0,0,0,31,0,0,0,31,0,0,0,0,0,0,0])
    deque2bfs = deque()
    deque2bfs.append(exampleProcess)
    while(deque2bfs):
        tempProcess = deque2bfs.popleft()
        if(len(tempProcess.candidateSeq)>0):
            tempResult = tempProcess.goForward()
            for item in tempResult:
                deque2bfs.append(item)
                # logging.info(item.board)
        else:
            logging.info(tempProcess.board)
            
    # When traversal Q98 notice that 32768s should be adjecent up and down on two rows
    # And rows with 32768s should not both have 4 elements
            
    
    
        

if (__name__ == "__main__"):
    traversal989694()