import numpy as np
import copy
import os
import logging
from collections import deque
import random

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='65536.log',  
    filemode='w'  
)

class Err65536(Exception):
    pass

def CalulateTotalPossibilities(str1):
    # ascii 40-126 are available in str1
    return (ord(str1[0])-40)*87 + (ord(str1[1])-40)
    
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
        

class FutureP:
    def __init__(self,str1):
        # *PCaseType[2]*CaseValue[2]*P[16]*SuccessRate[8]
        self.caseType = str1[0:2]
        self.caseValue = str1[2:4]
        self.pBoard = str1[4:20]
        self.successRate = str1[20:28]
        
class PastP:
    def __init__(self,str1):
        # *PCaseType[2]*CaseValue[2]*P[16]
        self.caseType = str1[0:2]
        self.caseValue = str1[2:4]
        self.pBoard = str1[4:20]
        
class Q:
    def __init__(self, str1):
        tempSplit = str1.split("!")
        '''
        *CaseType[2]
        !*CaseValue[2]
        !T*TotalPossibilites[2] （等于空位数×10，考虑所有出2和出4的情况）
        {!*Special*SuccessRate[8]}（*Special在特殊情况中是S，普通情况中是N）
        {!p*PCaseType[2]*CaseValue[2]*P[16]*SuccessRate[8]} （未来的P，可重复）
        {!P*PCaseType[2]CaseValue[2]*P[16]} （源自什么样的P可重复）
        '''
        self.caseType = tempSplit[0]
        self.caseValue = tempSplit[1]
        self.totalPossibilities = CalulateTotalPossibilities(tempSplit[2])
        self.specialCase = tempSplit[3][0]=="S"
        self.successRate = tempSplit[3][1:9]
        i = 4
        self.pastPList = []
        self.futurePList = []
        while(i<len(tempSplit)):
            if(tempSplit[i][0]=="p"):
                self.futurePListList.append(FutureP(tempSplit[i][1:]))
            elif(tempSplit[i][0]=="P"):
                self.pList.append(PastP(tempSplit[i][1:]))
            else:
                raise Err65536("Illegal Q string. The first letter of the section is NOT p or P")
        
class PlayP:
    def __init__(self,list1):
        # sanity check
        if(len(list1)!=16):
            raise Err65536("Illegal P list. The length is not 16")
        for i in range(16):
            if(not(-1/64 < list1[i] - int(list1[i]) < 1/64)):
                raise Err65536("Illegal P list. Non-integer value")
            if(not(0<=list1[i]<=31)):
                raise Err65536("Illegal P list. Out of range")
        # sanity check
        self.listBoard = list1[:]
        
        # definition
        # 0 stands for empty, 1-17 stands for 2-131072, 18-21 are stones, 22-31 stand for large numbers
        
    def transpose(self):
        temp0,temp1,temp2,temp3,temp4,temp5 = self.listBoard[1],self.listBoard[2],self.listBoard[3],self.listBoard[6],self.listBoard[7],self.listBoard[11]
        self.listBoard[1],self.listBoard[2],self.listBoard[3],self.listBoard[6],self.listBoard[7],self.listBoard[11] = self.listBoard[4],self.listBoard[8],self.listBoard[12],self.listBoard[9],self.listBoard[13],self.listBoard[14]
        self.listBoard[4],self.listBoard[8],self.listBoard[12],self.listBoard[9],self.listBoard[13],self.listBoard[14] = temp0,temp1,temp2,temp3,temp4,temp5
        
    def mirrorLr(self):
        tempRo1 = self.listBoard[0:4]
        tempRo1.reverse()
        tempRo2 = self.listBoard[4:8]
        tempRo2.reverse()
        tempRo3 = self.listBoard[8:12]
        tempRo3.reverse()
        tempRo4 = self.listBoard[12:16]
        tempRo4.reverse()
        self.listBoard = tempRo1 + tempRo2 + tempRo3 + tempRo4
        
    def transposeDl(self):
        temp0,temp1,temp2,temp3,temp4,temp5 = self.listBoard[0],self.listBoard[1],self.listBoard[2],self.listBoard[4],self.listBoard[5],self.listBoard[8]
        self.listBoard[0],self.listBoard[1],self.listBoard[2],self.listBoard[4],self.listBoard[5],self.listBoard[8] = self.listBoard[15],self.listBoard[11],self.listBoard[7],self.listBoard[14],self.listBoard[10],self.listBoard[13]
        self.listBoard[15],self.listBoard[11],self.listBoard[7],self.listBoard[14],self.listBoard[10],self.listBoard[13] = temp0,temp1,temp2,temp3,temp4,temp5
    
    def goLeft(self):
        listBackup = self.listBoard[:]
        
        # extract rows
        listResult = []
        for ro in range(4):
            dequeRo = deque(self.listBoard[ro*4:(ro+1)*4])
            tempConnect = 0
            listResultRo = []
            while(dequeRo):
                popLeft = dequeRo.popleft()
                if(popLeft == 0):
                    continue
                if(popLeft == tempConnect and popLeft not in [17,18,19,20,31]):
                    tempConnect = 0
                    listResultRo[-1] += 1
                else:
                    tempConnect = popLeft
                    listResultRo.append(popLeft)
            while(len(listResultRo)<4):
                listResultRo.append(0)
            listResult.extend(listResultRo)
        # extract rows
        
        self.listBoard = listResult[:]
        
        if(listBackup == listResult):
            return False
        else:
            # choose a block with value 0 at random
            tempZeroList = []
            for i in range(16):
                if(self.listBoard[i] == 0):
                    tempZeroList.append(i)
            randomIndex = random.choice(tempZeroList)
            random2or4 = random.randint(1,10)
            if(random2or4 <= 9):
                self.listBoard[randomIndex] = 1
            else:
                self.listBoard[randomIndex] = 2
            return True
    
    def goUp(self):
        self.transpose()
        tempBool = self.goLeft()
        self.transpose()
        return tempBool
    
    def goRight(self):
        self.mirrorLr()
        tempBool = self.goLeft()
        self.mirrorLr()
        return tempBool
    
    def goDown(self):
        self.transposeDl()
        tempBool = self.goLeft()
        self.transposeDl()
        return tempBool
    
    def printBoard(self):
        tempMapSpace = [6,6,6,6, 5,5,5, 4,4,4, 3,3,3,3, 2,2,2, 1, 2,2,2, 4,4,4,4,4,4,4,4,4,4,4]
        tempMapStr = ["X","2","4","8","16","32","64","128","256","512","1024","2048","4096","8192","16384","32768","65536","131072"]
        tempMapStr = tempMapStr + ["stone","stone","stone"]
        tempMapStr = tempMapStr + ["s21","s22","s23","s24","s25","s26","s27","s28","s29","s30","s31"]
        for i in range(32):
            tempStr = tempMapStr[i]
            for j in range(tempMapSpace[i]):
                tempStr = tempStr + " "
            tempMapStr[i] = tempStr
        print(tempMapStr[self.listBoard[0]]+tempMapStr[self.listBoard[1]]+tempMapStr[self.listBoard[2]]+tempMapStr[self.listBoard[3]]+"\012")
        print(tempMapStr[self.listBoard[4]]+tempMapStr[self.listBoard[5]]+tempMapStr[self.listBoard[6]]+tempMapStr[self.listBoard[7]]+"\012")
        print(tempMapStr[self.listBoard[8]]+tempMapStr[self.listBoard[9]]+tempMapStr[self.listBoard[10]]+tempMapStr[self.listBoard[11]]+"\012")
        print(tempMapStr[self.listBoard[12]]+tempMapStr[self.listBoard[13]]+tempMapStr[self.listBoard[14]]+tempMapStr[self.listBoard[15]]+"\012")


if __name__ == '__main__':
    tempList = [1,0,0,0, 3,0,0,0, 2,0,0,0, 4,0,0,0]
    playP = PlayP(tempList)
    print(playP.goDown())
    playP.printBoard()
        
    