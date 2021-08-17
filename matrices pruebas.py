from hashlib import new
from math import cos, sin, pi
import struct
from collections import namedtuple

import numpy as np
from numpy.testing._private.utils import print_assert_equal

V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])


def multyMatrix (Matrix, Matrix2):
    matrix1Row = len(Matrix)
    matrix2RowLimit = len(Matrix2[0])
    newMatrix = []
    for y in range(matrix1Row):
        newRow = []
        matrix2Row = 0
        matrix2Col = len(Matrix2)
        column1 = 0
        for x in range(matrix1Row):
            for i in range(matrix2Col):
                #print(Matrix[y][(x+i) % matrix2Col],  Matrix2[(x+i) % matrix2Col][matrix2Row])
                column1 = (Matrix[y][(x+i) % matrix2Col] * Matrix2[(x+i) % matrix2Col][matrix2Row]) + column1
            #print(column1)
            if matrix2RowLimit == 1:
                newMatrix.append(column1)
                break
            matrix2Row += 1
            newRow.append(column1)
            column1 = 0
        if matrix2RowLimit != 1:
            newMatrix.append(newRow)
    #print(newMatrix)
    return newMatrix

def multiVecMatrix(Vector, Matrix):
    matrix1Row = len(Matrix)
    matrixColumns = len(Matrix[0])
    newVector = []
    for y in range(matrix1Row):
        newNumber = 0
        vectorCol = 0
        for x in range(matrixColumns):
            #print(Matrix[y][x], Vector[vectorCol])
            newNumber = (Matrix[y][x] * Vector[vectorCol]) + newNumber
            vectorCol += 1
        newVector.append(newNumber)
    #print(newVector)
    return(newVector)




hola = [[1,0,3,4],
        [3,1,2,1],
        [2,3,1,5],
        [6,0,3,1]]

hola4 = [[7],
        [9],
        [11],
        [2]]

hola5 = V4(7,9,11,2)

multiVecMatrix(hola5, hola)

hola2 = [[1,3,0,0],
                   [0,1,6,7],
                   [0,3,1,0],
                   [3,0,4,1]]

hola3 = np.matrix([[0,2,0,0],
                   [3,0,3,6],
                   [0,4,0,0],
                   [6,0,5,0]])
multyMatrix(hola, hola2)


#print(hola * hola2 * hola3)



#hola3 = [[1,2,3],
     #   [4,5,6]]

#hola4 = [[7,8],
    #    [9,10],
    #    [11,12]]

#multyMatrix(hola, hola2)

#for y in hola:
#    #print(y, len(hola[y]))
#    for x in y:
#        x = 5 
#       
#print (hola)

