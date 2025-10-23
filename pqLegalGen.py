import numpy as np
import copy
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='65536.log',  
    filemode='w'  
)

def GenerateQLegal():
    logging.info('Starting program')
    qCanFromUp =[]
    qCanFromDown = []
    qCanFromLeft = []
    qCanFromRight = []
    qCanFromExist = []
    for traversal in range(65536):
        tempBoard = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        temp = traversal
        for j in range(16):
            tempBoard[j//4][j%4] = temp%2
            temp = temp//2

        tempCanFromUp = True
        for i in range(3):
            for j in range(4):
                if(tempBoard[i][j] == 0 and tempBoard[i+1][j] != 0):
                    tempCanFromUp = False
                    break
        
        tempCanFromDown = True
        for i in range(1,4):
            for j in range(4):
                if(tempBoard[i][j] == 0 and tempBoard[i-1][j] != 0):
                    tempCanFromDown = False
                    break
        
        tempCanFromLeft = True
        for i in range(4):
            for j in range(3):
                if(tempBoard[i][j] == 0 and tempBoard[i][j+1] != 0):
                    tempCanFromLeft = False
                    break
                
        tempCanFromRight = True
        for i in range(4):
            for j in range(1,4):
                if(tempBoard[i][j] == 0 and tempBoard[i][j-1] != 0):
                    tempCanFromRight = False
                    break

        if(tempCanFromUp or tempCanFromDown or tempCanFromLeft or tempCanFromRight):
            tempCanFromExist = True
        else:
            tempCanFromExist = False
            
        # calculate how many squares are occupied 
        tempOccupied = 0
        for i in range(16):
            if(traversal & (1 << i)):
                tempOccupied += 1
            
        if(tempCanFromUp):
            qCanFromUp.append((traversal,tempOccupied))
            
        if(tempCanFromDown):
            qCanFromDown.append((traversal,tempOccupied))
            
        if(tempCanFromLeft):
            qCanFromLeft.append((traversal,tempOccupied))
            
        if(tempCanFromRight):
            qCanFromRight.append((traversal,tempOccupied))

        if(tempCanFromExist):
            qCanFromExist.append((traversal,tempOccupied))
            
    with open ('./qLegal/up.txt', 'w' ) as f:
        for item in qCanFromUp:
            f.write(str(str(item[0]) + ' ' + str(item[1]) + '\n'))
            
    with open ('./qLegal/down.txt', 'w' ) as f:
        for item in qCanFromDown:
            f.write(str(str(item[0]) + ' ' + str(item[1]) + '\n'))
            
    with open ('./qLegal/left.txt', 'w' ) as f:
        for item in qCanFromLeft:
            f.write(str(str(item[0]) + ' ' + str(item[1]) + '\n'))
            
    with open ('./qLegal/right.txt', 'w' ) as f:
        for item in qCanFromRight:
            f.write(str(str(item[0]) + ' ' + str(item[1]) + '\n'))
            
    with open ('./qLegal/exist.txt', 'w' ) as f:
        for item in qCanFromExist:
            f.write(str(str(item[0]) + ' ' + str(item[1]) + '\n'))
            
            
# TODO generate pTraversal
# p<-q for each p, what q is it? Or which block can be the adding block?
def GeneratePLegal():
    # check if qLeagal exists
    try:
        with open("./qLegal/exist.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("qLegal does not exist")
        return
    
    resultToW = []
    resultToWClassified = [[] for _ in range(17)]
    # go for "0 1 4 + 15" like format
    for line in lines:
        # split the line by space
        tempSplit = line.split()
        # get the first element
        qMask = int(tempSplit[0])
        if(qMask == 0 or qMask == 65535):
            continue
        tempStr = ""
        tempList = []
        for i in range(0,16):
            if(qMask & (1 << i)):
                tempStr += str(i) + " "
                tempList.append(i)
        tempStr += "+ "
        
        for i in range(16):
            if(i not in tempList):
                resultToW.append(tempStr + str(i))
    
    # classify from resultToW to resultToWClassified
    for item in resultToW:
        resultToWClassified[len(item.rstrip().split())-1].append(item)
                
    try:
        for i in range(1,17):
            with open("./pLegal/exist"+str(i)+".txt", "w") as f:
                for item in resultToWClassified[i]:
                    f.write(str(item) + '\n')
    except FileNotFoundError:
        print("pLegal does not exist")
        
        
if __name__ == '__main__':
    GenerateQLegal()