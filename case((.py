import board
import sumTraversal

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
    dequeSum98 = sumTraversal.traversalFunc(98, 2)
    while(len(dequeSum98) > 0):
        tempSum = dequeSum98.popleft()
        # calculate how many blocks should be used.
        # first calculate the overall sum of the list tempSum
        tempBlocksUsed = sum(tempSum) + 2
        for permutation in qUp[tempBlocksUsed]:
            # do something
            pass
        for permutation in qDown[tempBlocksUsed]:
            # do something
            pass
        for permutation in qLeft[tempBlocksUsed]:
            # do something
            pass
        for permutation in qRight[tempBlocksUsed]:
            # do something
            pass

if (__name__ == "__main__"):
    pass