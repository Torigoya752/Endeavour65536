import numpy as np
import copy
import os
import logging
import board
import sumTraversal

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='65536.log',  
    filemode='w'  
)

class Err65536(Exception):
    pass

def genQ118():
    # from board.QCANFROMUP classify according to the number of numbers in the board
    # 0: empty, 1: 1 number, 2: 2 numbers, 3: 3 numbers, 4: 4 numbers, 5: 5 numbers, 6: 6 numbers
    qCanFromUpClassified = [[] for _ in range(16)]
    

if __name__ == '__main__':
    sumTraversal.traversalFunc(118,3)