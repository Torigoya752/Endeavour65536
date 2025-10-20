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

class Q:
    def __init__(self, list_1, rate):
        self.board = copy.deepcopy(list_1)
        self.rate = rate
        self.canFromUp = True
        self.canFromDown = True
        self.canFromLeft = True
        self.canFromRight = True
        
    def tryFromUp(self):
        for i in range(3):
            for j in range(4):
                if(self.board[i][j] == 0 and self.board[i+1][j] != 0):
                    self.canFromUp = False
                    break
                
        for j in range(4):
            if(self.board[2][j]!= 0 and self.board[3][j] == 0 and self.board[0][j] == self.board[1][j] and self.board[1][j] == self.board[2][j]):
                self.canFromUp = False
                break
            if(self.board[3][j] != 0 and (self.board[0][j] == self.board[1][j] or self.board[1][j] == self.board[2][j] or self.board[2][j] == self.board[3][j])):
                self.canFromUp = False
                break
            
    def tryFromDown(self):
        for i in range(1,4):
            for j in range(4):
                if(self.board[i][j] == 0 and self.board[i-1][j] != 0):
                    self.canFromDown = False
                    break
                
        for j in range(4):
            if(self.board[1][j]!= 0 and self.board[0][j] == 0 and self.board[2][j] == self.board[3][j] and self.board[1][j] == self.board[2][j]):
                self.canFromDown = False
                break
            if(self.board[0][j] != 0 and (self.board[1][j] == self.board[2][j] or self.board[2][j] == self.board[3][j] or self.board[1][j] == self.board[0][j])):
                self.canFromDown = False
                break
                
    def tryFromLeft(self):
        for i in range(4):
            for j in range(3):
                if(self.board[i][j] == 0 and self.board[i][j+1] != 0):
                    self.canFromLeft = False
                    break
                
        for i in range(4):
            if(self.board[i][2] != 0 and self.board[i][0] == 0 and self.board[i][1] == self.board[i][2]):
                self.canFromLeft = False
                break
            if(self.board[i][3] != 0 and (self.board[i][1] == self.board[i][2] or self.board[i][2] == self.board[i][3] or self.board[i][1] == self.board[i][0])):
                self.canFromLeft = False
                break
                
    def tryFromRight(self):
        for i in range(4):
            for j in range(1,4):
                if(self.board[i][j] == 0 and self.board[i][j-1] != 0):
                    self.canFromRight = False
                    break
                
        for i in range(4):
            if(self.board[i][1] != 0 and self.board[i][3] == 0 and self.board[i][2] == self.board[i][1]):
                self.canFromRight = False
                break
            if(self.board[i][0] != 0 and (self.board[i][2] == self.board[i][1] or self.board[i][1] == self.board[i][0] or self.board[i][2] == self.board[i][3])):
                self.canFromRight = False
                break
        
        


if __name__ == '__main__':
    a = [[1,2],[3,4]]
    b = copy.deepcopy(a)
    a[0][0] = 5
    logging.info(b)