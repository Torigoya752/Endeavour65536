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

class Err65536(Exception):
    pass

# load qLegal
with open ("./qLegal/up.txt", "r") as f:
    lines = f.readlines()
QCANFROMUP = []
for line in lines:
    QCANFROMUP.append(int(line.rstrip()))


# down
with open ("./qLegal/down.txt", "r") as f:
    lines = f.readlines()
QCANFROMDOWN = []
for line in lines:
    QCANFROMDOWN.append(int(line.rstrip()))


# left
with open ("./qLegal/left.txt", "r") as f:
    lines = f.readlines()
QCANFROMLEFT = []
for line in lines:
    QCANFROMLEFT.append(int(line.rstrip()))


# right
with open ("./qLegal/right.txt", "r") as f:
    lines = f.readlines()
QCANFROMRIGHT = []
for line in lines:
    QCANFROMRIGHT.append(int(line.rstrip()))
    
# exist
with open ("./qLegal/exist.txt", "r") as f:
    lines = f.readlines()
QEXIST = []
for line in lines:
    QEXIST.append(int(line.rstrip()))


class Q:
    def __init__(self, list_1, rate):
        self.board = copy.deepcopy(list_1)
        self.rate = rate
        self.canFromUp = True
        self.canFromDown = True
        self.canFromLeft = True
        self.canFromRight = True
        self.containNumberMask = 0
        for i in range(4):
            for j in range(4):
                if(self.board[i][j] != 0):
                    self.containNumberMask += (1 << (i*4 + j))
        
    def tryFromUp(self):
        if(self.containNumberMask not in QCANFROMUP):
            self.canFromUp = False
            return
                
        for j in range(4):
            if(self.board[2][j]!= 0 and self.board[3][j] == 0 and self.board[0][j] == self.board[1][j] and self.board[1][j] == self.board[2][j]):
                self.canFromUp = False
                return
            if(self.board[3][j] != 0 and (self.board[0][j] == self.board[1][j] or self.board[1][j] == self.board[2][j] or self.board[2][j] == self.board[3][j])):
                self.canFromUp = False
                return
            
    def tryFromDown(self):
        if(self.containNumberMask not in QCANFROMDOWN):
            self.canFromDown = False
            return
                
        for j in range(4):
            if(self.board[1][j]!= 0 and self.board[0][j] == 0 and self.board[2][j] == self.board[3][j] and self.board[1][j] == self.board[2][j]):
                self.canFromDown = False
                return
            if(self.board[0][j] != 0 and (self.board[1][j] == self.board[2][j] or self.board[2][j] == self.board[3][j] or self.board[1][j] == self.board[0][j])):
                self.canFromDown = False
                return
                
    def tryFromLeft(self):
        if(self.containNumberMask not in QCANFROMLEFT):
            self.canFromLeft = False
            return
                
        for i in range(4):
            if(self.board[i][2] != 0 and self.board[i][0] == 0 and self.board[i][1] == self.board[i][2]):
                self.canFromLeft = False
                return
            if(self.board[i][3] != 0 and (self.board[i][1] == self.board[i][2] or self.board[i][2] == self.board[i][3] or self.board[i][1] == self.board[i][0])):
                self.canFromLeft = False
                return
                
    def tryFromRight(self):
        if(self.containNumberMask not in QCANFROMRIGHT):
            self.canFromRight = False
            return
                
        for i in range(4):
            if(self.board[i][1] != 0 and self.board[i][3] == 0 and self.board[i][2] == self.board[i][1]):
                self.canFromRight = False
                return
            if(self.board[i][0] != 0 and (self.board[i][2] == self.board[i][1] or self.board[i][1] == self.board[i][0] or self.board[i][2] == self.board[i][3])):
                self.canFromRight = False
                return
        
        


if __name__ == '__main__':
    a = [[1,2],[3,4]]
    b = copy.deepcopy(a)
    a[0][0] = 5
    logging.info(b)