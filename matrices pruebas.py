from hashlib import new
from math import cos, sin, pi
import math
import struct
from collections import namedtuple

import numpy as np
from numpy.lib.function_base import piecewise
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

hola4 = [[7],
        [9],
        [11],
        [2]]

hola5 = V4(7,9,11,2)

#multiVecMatrix(hola5, hola)

hola2 = [[1,3,0,0],
                   [0,1,6,7],
                   [0,3,1,0],
                   [3,0,4,1]]

hola3 = [[0,2,0],
         [3,0,3],
         [0,4,0]]

hola7 = [[1,2,3],
         [4,5,6],
         [7,8,9]]
#multyMatrix(hola, hola2)


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

def createMatrix(row, col, listOfLists, multi = 1):
    matrix = []
    for i in range(row):
        
        rowList = []
        for j in range(col):
            
            # you need to increment through dataList here, like this:
            rowList.append((listOfLists[row * i + j]) * multi)    
                    
        matrix.append(rowList)
    
    return matrix

def transpose(matrix):
    rows = len(matrix)
    columns = len(matrix[0])

    matrix_T = []
    for j in range(columns):
        row = []
        for i in range(rows):
           row.append(matrix[i][j])
        matrix_T.append(row)

    return matrix_T

def determinante3X3(matrix):
    rows = len(matrix)
    columns = len(matrix[0])
    newMatrix = []
    for y in range(rows):
        newRow = []
        for x in range(columns):
            if x == 2:
                #print(matrix[y][x], matrix[y][(x + 1) % columns], matrix[y][(x + 2) % columns])
                newRow.extend([matrix[y][x], matrix[y][(x + 1) % columns], matrix[y][(x + 2) % columns]])
                break
            newRow.append(matrix[y][x])
        newMatrix.append(newRow)
    #print(newMatrix)
    diagonal1 = 0
    diagonal2 = 0
    for x in range(columns):
        diagonal1 = (newMatrix[0][x] * newMatrix[1][x+1] * newMatrix[2][x+2]) + diagonal1
        diagonal2 = -(newMatrix[0][x+2] * newMatrix[1][x+1] * newMatrix[2][x]) + diagonal2
        #print(newMatrix[0][x], newMatrix[1][x+1], newMatrix[2][x+2])
        #print(newMatrix[0][x+2], newMatrix[1][x+1], newMatrix[2][x])
    determinante = diagonal1 + diagonal2
    return determinante

def inversa4X4(Matrix):
    newMatrix = transpose(Matrix)
    #print(newMatrix)
    row = len(Matrix[0])
    column = len(Matrix)
    determinant = 0
    cofactorList = []
    for y in range(row):
        exponent1 = y + 1
        for x in range(column):
            exponent2 = x + 1
            exponentT = exponent2 + exponent1
            cofactorM = []
            if y == 0:
                detM = []
            verificador = False
            for i in range(row):
                if y == 0:
                    rowDe = []    
                rowCo = []
                for k in range(column):
                    if i != y and x != k:
                        #print("y: ",y, "i: ",i, "x: ",x, "k: ",k)
                        #print(Matrix[i][k])
                        verificador = True
                        rowCo.append(newMatrix[i][k])
                        if y == 0:
                            rowDe.append(Matrix[i][k])
                if verificador:
                    if y == 0:
                        detM.append(rowDe)
                    cofactorM.append(rowCo)
                    verificador = False
            #print(cofactorM)
            #print(detM)
            #print((-1) ** exponentT)
            deter = ((-1) ** exponentT) * determinante3X3(cofactorM)
            cofactorList.append(deter)
            if y == 0: 
               deter2 = ((-1) ** exponentT) * determinante3X3(detM)
               determinant = (Matrix[y][x] * deter2) + determinant
    print(determinant)
    Inverse = createMatrix(4, 4, cofactorList, (1/determinant))
    #print(Inverse)
    return Inverse

hola = [[1,0,3,4],
        [3,1,2,1],
        [2,3,1,5],
        [6,0,3,1]]

hols = [[1,3,2,6],
        [0,1,3,0],
        [3,2,1,3],
        [4,1,5,1]]

eje =  [[2,1,-3,2],
        [-4,2,4,-1],
        [-2,1,1,4],
        [1,-2,-1,4]]

eje3 =  [[1,1,0,0],
        [0,-1,-2,0],
        [0,0,1,-1],
        [0,0,0,1]]

inversa = inversa4X4(eje3)
print(inversa)

eje2 = [1,2,3,4,5,6,7,8,9]

#createMatrix(3, 3, eje2, 2)

#hola7 = transpose(hola3)
#print(hola7)
#print(hola3)