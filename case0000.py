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
    caseNumQ62 = 0

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
    # class bfsProcess
    
    # test with a small case
    # ex: - root - INFO - [5, 4, 3, 1] [1, 3, 2, 1] 0 [0, 1, 2, 3, 8, 9, 12, 13, 14] [0, 3, 3, 3, 0, 1, 0, 1, 2] [0, 0, 0, 0, 0, 0, 0, 0, 31, 0, 0, 0, 31, 0, 0, 0]
    exampleProcess = bfsProcess([5,4,3,1],[1,3,2,1],0,[0, 1, 2, 3, 8, 9, 12, 13, 14],[0, 3, 3, 3, 0, 1, 0, 1, 2],[0, 0, 0, 0, 0, 0, 0, 0, 31, 0, 0, 0, 31, 0, 0, 0])
    deque2bfs = deque()
    deque2bfs.append(exampleProcess)
    while(deque2bfs):
        tempProcess = deque2bfs.popleft()
        if(len(tempProcess.candidateSeq)>0):
            tempResult = tempProcess.goForward()
            for item in tempResult:
                deque2bfs.append(item)
        else:
            # logging.info(tempProcess.board)
            pass
    # test with a small case
            
    # When traversal Q98
    # I 32768 connect horizantally -> It is from a P 32768-16384-16384 or something like that
    # II 32768 connect vertically -> the two rows with 32768 should not both have 4 elements
    # In either case, discard cases with two 32768s in the middle of the board and 8 or more numbers on the board
    # listCase0001P78 = []
    
    # traversal all Q98 permutations
    dequeSum98 = sumTraversal.traversalFunc(62, 2)
    # print(len(dequeSum98))
    # traversal all Q98 permutations
    
    
    # open the left.txt and make a list, the index of which contains all available boards
    listTwo32768AvailableQLeftBoards = [[] for _ in range(17)]
    with open('./qLegal/left.txt', 'r', encoding='utf-8') as f:
        tempLines = f.readlines()
    for line in tempLines:
        tempSplit = line.rstrip().split()
        tempNumbersOnBoard = int(tempSplit[1])
        tempBoardPasscode = int(tempSplit[0])
        tempList = []
        for i in range(16):
            if(tempBoardPasscode & (1 << i)):
                tempList.append(i)
        listTwo32768AvailableQLeftBoards[tempNumbersOnBoard].append(tempList[:])
    # print(listTwo32768AvailableQLeftBoards[6])
    # open the left.txt and make a list, the index of which contains all available boards
    
    # traversal dequeSum98 and pair each case with some available boards
    listBoardQ98 = []
    while(len(dequeSum98) != 0):
        tempListSum98 = dequeSum98.popleft()
        tempNumbersOnBoard = sum(tempListSum98) + 2
        
        if(tempNumbersOnBoard >= 14):
            continue
        
        # generate tempCandidateSeq and tempCandidateNumLeft
        # ex: [0, 0, 0, 0, 0, 12, 0, 1] -> seq[3,1], numLeft[12,1]
        tempCandidateSeq = []
        tempCandidateNumLeft = []
        for i in range(8):
            if(tempListSum98[i] != 0):
                tempCandidateSeq.append(8-i)
                tempCandidateNumLeft.append(tempListSum98[i])
        # generate tempCandidateSeq and tempCandidateNumLeft
        
        # generate tempNextIndexToFill
        tempNextIndexToFill = 0
        # generate tempNextIndexToFill
        
        # tempListsum98 is the sum list being traversed
        # logging.info(str(tempListSum98))
        for tempListPositionsToFill in listTwo32768AvailableQLeftBoards[tempNumbersOnBoard]:
            
            # count how many numbers emerge in each row
            tempListRowNumbers = [0, 0, 0, 0]
            for item in tempListPositionsToFill:
                tempListRowNumbers[item // 4] += 1
            # count how many numbers emerge in each row
            
            # generate the listBanLevel
            tempListBanLevel = []
            for item in tempListRowNumbers:
                if(item == 1):
                    tempListBanLevel.append(0)
                elif(item == 2):
                    tempListBanLevel = tempListBanLevel + [0,1]
                elif(item == 3):
                    tempListBanLevel = tempListBanLevel + [0,1,2]
                elif(item == 4):
                    tempListBanLevel = tempListBanLevel + [0,3,3,3]
            # generate the listBanLevel
            
            # traversal 0-15, locate the upper 32768, then go down until the other square to locate 32768 is found
            for tempUpper32768 in tempListPositionsToFill:
                tempDowner32768 = tempUpper32768 + 4
                while(tempDowner32768 < 16):
                    if(tempDowner32768 in tempListPositionsToFill):
                        break
                    tempDowner32768 += 4
                if(tempDowner32768 < 16 and not(tempListRowNumbers[tempUpper32768 // 4] == 4 and tempListRowNumbers[tempDowner32768 // 4] == 4)):
                    # delete cases with two 32768s in the centre
                    if((tempUpper32768 == 5 and tempDowner32768 == 9) or (tempUpper32768 == 6 and tempDowner32768 == 10)):
                        continue
                    # delete cases with two 32768s in the centre
                    
                    # logging.info("----"+str(tempListSum98)+str(tempListPositionsToFill)+str((tempUpper32768, tempDowner32768)))
                    # feed them into the bfs system 
                    tempListBoard = [0 for _ in range(16)]
                    tempListBoard[tempUpper32768] = 31
                    tempListBoard[tempDowner32768] = 31
                    # logging.info(str(tempCandidateSeq)+" "+str(tempCandidateNumLeft)+" "+str(tempNextIndexToFill) + " " + str(tempListPositionsToFill) + " " + str(tempListBanLevel) +" " + str(tempListBoard))
                    tempDeque2bfs = deque()
                    tempDeque2bfs.append(bfsProcess(tempCandidateSeq, tempCandidateNumLeft, tempNextIndexToFill, tempListPositionsToFill, tempListBanLevel, tempListBoard))
                    while(tempDeque2bfs):
                        tempProcess = tempDeque2bfs.popleft()
                        if(len(tempProcess.candidateSeq) > 0):
                            tempResult = tempProcess.goForward()
                            for item in tempResult:
                                tempDeque2bfs.append(item)
                        else:
                            listBoardQ98.append(tempProcess.board[:])
                            caseNumQ62 += 1
                    # feed them into the bfs system
            # traversal 0-15, locate the upper 32768, then go down until the other square to locate 32768 is found
    logging.info(caseNumQ62)
        

if (__name__ == "__main__"):
    traversal989694()