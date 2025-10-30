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
'''
# load qLegal
with open ("./qLegal/up.txt", "r") as f:
    lines = f.readlines()
qCanFromUpList = []
for line in lines:
    qCanFromUpList.append(int(line.rstrip()[0]))
QCANFROMUP = tuple(qCanFromUpList)

# down
with open ("./qLegal/down.txt", "r") as f:
    lines = f.readlines()
qCanFromDownList = []
for line in lines:
    qCanFromDownList.append(int(line.rstrip()[0]))
QCANFROMDOWN = tuple(qCanFromDownList)


# left
with open ("./qLegal/left.txt", "r") as f:
    lines = f.readlines()
qCanFromLeftList = []
for line in lines:
    qCanFromLeftList.append(int(line.rstrip()[0]))
QCANFROMLEFT = tuple(qCanFromLeftList)

# right
with open ("./qLegal/right.txt", "r") as f:
    lines = f.readlines()
qCanFromRightList = []
for line in lines:
    qCanFromRightList.append(int(line.rstrip()[0]))
QCANFROMRIGHT = tuple(qCanFromRightList)
    
# exist
with open ("./qLegal/exist.txt", "r") as f:
    lines = f.readlines()
qExistList = []
for line in lines:
    qExistList.append(int(line.rstrip()[0]))
QEXIST = tuple(qExistList)
'''    
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
        
        
        
    
        
        


if __name__ == '__main__':
    a = [[1,2],[3,4]]
    b = copy.deepcopy(a)
    a[0][0] = 5
    logging.info(b)