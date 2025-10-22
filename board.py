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
    
class P:
    def __init__(self,str1):
        tempSplit = str1.rstrip().split("!")
        '''
        *CaseType[2]
        !*CaseValue[2](每个类型的具体值，如“并1，+254”中的“254”）
        {!S*SuccessRate[8]}（仅出现在p类是特殊的类，用8个字符表示成功率）
        {!B*Direction[1]*QCaseType[2]CaseValue[2]*Q[16]*SuccessRate[8]} （当且仅当算出了最好的一步，用1个字符表示方向，8个字符）
        {!U*QCaseType[2]CaseValue[2]*Q[16]*SuccessRate[8]} （往上移动，往下往左往右同理，此处省略）
        {!Q*QCaseType[2]CaseValue[2]*Q[16]} （源自哪个Q）
        '''
        self.caseType = tempSplit[0]
        self.caseValue = tempSplit[1]
        i = 2
        if(i<len(tempSplit) and tempSplit[i][0] == "S"):
            self.specialP = True
            self.successRate = tempSplit[i][1:]
            i += 1
        else:
            self.specialP = False
            self.successRate = None
            
        if(i<len(tempSplit) and tempSplit[i][0] == "B"):
            self.bestValid = True
            self.bestDirection = tempSplit[i][1]
            self.bestQCaseType = tempSplit[i][2:4]
            self.bestQCaseValue = tempSplit[i][4:6]
            self.bestQBoard = tempSplit[i][6:22]
            self.bestSuccessRate = tempSplit[i][22:30]
            i += 1
        else:
            self.bestValid = False
            self.bestDirection = None
            self.bestQCaseType = None
            self.bestQCaseValue = None
            self.bestQBoard = None
            self.bestSuccessRate = None
            
        if(i<len(tempSplit) and tempSplit[i][0] == "U"):
            self.uValid = True
            self.uQCaseType = tempSplit[i][1:3]
            self.uQCaseValue = tempSplit[i][3:5]
            self.uQBoard = tempSplit[i][5:21]
            self.uSuccessRate = tempSplit[i][21:29]
            i += 1
        else:
            self.uValid = False
            self.uQCaseType = None
            self.uQCaseValue = None
            self.uQBoard = None
            self.uSuccessRate = None
            
        if(i<len(tempSplit) and tempSplit[i][0] == "D"):
            self.dValid = True
            self.dQCaseType = tempSplit[i][1:3]
            self.dQCaseValue = tempSplit[i][3:5]
            self.dQBoard = tempSplit[i][5:21]
            self.dSuccessRate = tempSplit[i][21:29]
            i += 1
        else:
            self.dValid = False
            self.dQCaseType = None
            self.dQCaseValue = None
            self.dQBoard = None
            self.dSuccessRate = None
            
        if(i<len(tempSplit) and tempSplit[i][0] == "L"):
            self.lValid = True
            self.lQCaseType = tempSplit[i][1:3]
            self.lQCaseValue = tempSplit[i][3:5]
            self.lQBoard = tempSplit[i][5:21]
            self.lSuccessRate = tempSplit[i][21:29]
            i += 1
        else:
            self.lValid = False
            self.lQCaseType = None
            self.lQCaseValue = None
            self.lQBoard = None
            self.lSuccessRate = None
            
        if(i<len(tempSplit) and tempSplit[i][0] == "R"):
            self.rValid = True
            self.rQCaseType = tempSplit[i][1:3]
            self.rQCaseValue = tempSplit[i][3:5]
            self.rQBoard = tempSplit[i][5:21]
            self.rSuccessRate = tempSplit[i][21:29]
            i += 1
        else:
            self.rValid = False
            self.rQCaseType = None
            self.rQCaseValue = None
            self.rQBoard = None
            self.rSuccessRate = None
            
        self.qList = []
        
        if(i<len(tempSplit)):
            self.possessSourceQ = True
        else:
            self.possessSourceQ = False # TODO it should be a dead case. Do NOT genetate the P
        
        while(i<len(tempSplit)):
            if(tempSplit[i][0]!="Q"):
                raise Err65536("Illegal P string. The capital of the last section is NOT Q")
            # for each element in qList, just write *QCaseType[2]CaseValue[2]*Q[16]
            self.qList.append(tempSplit[i][1:21])
            i+=1
        


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