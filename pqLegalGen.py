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

def main():
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
            
        if(tempCanFromUp):
            qCanFromUp.append(traversal)
            
        if(tempCanFromDown):
            qCanFromDown.append(traversal)
            
        if(tempCanFromLeft):
            qCanFromLeft.append(traversal)
            
        if(tempCanFromRight):
            qCanFromRight.append(traversal)

        if(tempCanFromExist):
            qCanFromExist.append(traversal)
            
    with open ('./qLegal/up.txt', 'w' ) as f:
        for item in qCanFromUp:
            f.write(str(item) + '\n')
            
    with open ('./qLegal/down.txt', 'w' ) as f:
        for item in qCanFromDown:
            f.write(str(item) + '\n')
            
    with open ('./qLegal/left.txt', 'w' ) as f:
        for item in qCanFromLeft:
            f.write(str(item) + '\n')
            
    with open ('./qLegal/right.txt', 'w' ) as f:
        for item in qCanFromRight:
            f.write(str(item) + '\n')
            
    with open ('./qLegal/exist.txt', 'w' ) as f:
        for item in qCanFromExist:
            f.write(str(item) + '\n')
            
# TODO generate pTraversal
# p<-q for each p, what q is it? Or which block can be the adding block?
        
        
if __name__ == '__main__':
    pass