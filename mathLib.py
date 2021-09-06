from collections import namedtuple
from math import pi

V3 = namedtuple('Point3', ['x', 'y', 'z'])

def sub(v0, v1):
  
  return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def dot(v0, v1):
  
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def mul(v0, k):
  
  return V3(v0.x * k, v0.y * k, v0.z *k)

def cross(v0, v1):
  
  return V3(
    v0.y * v1.z - v0.z * v1.y,
    v0.z * v1.x - v0.x * v1.z,
    v0.x * v1.y - v0.y * v1.x,
  )

def length(v0):
 
  return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):

  v0length = length(v0)

  if not v0length:
    return V3(0, 0, 0)

  return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

def baryCoords(A, B, C, P):
    # u es para A, v es para B, w es para C
    try:
        #PCB/ABC
        u = (((B.y - C.y) * (P.x - C.x) + (C.x - B.x) * (P.y - C.y)) /
            ((B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y))) 

        #PCA/ABC
        v = (((C.y - A.y) * (P.x - C.x) + (A.x - C.x) * (P.y - C.y)) /
            ((B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y))) 

        w = 1 - u - v
    except: 
        return -1, -1, -1

    return u, v, w

def radDegrees(radianes):
    return radianes * (180/pi)

def degreesRad(grados):
    return grados * (pi/180)

#Multiplicacion de matrices
def multyMatrix4X4 (Matrix, Matrix2):
    matrix1Row = len(Matrix)
    matrix1Col = len(Matrix[0])
    newMatrix = []
    for y in range(matrix1Col):
        newRow = []
        matrix2Row = 0
        column1 = 0
        column2 = 0
        column3 = 0
        column4 = 0
        for x in range(matrix1Row):
            column1 = (Matrix[y][x] * Matrix2[x][matrix2Row]) + column1
            column2 = (Matrix[y][x] * Matrix2[x][matrix2Row + 1]) + column2
            column3 = (Matrix[y][x] * Matrix2[x][matrix2Row + 2]) + column3
            column4 = (Matrix[y][x] * Matrix2[x][matrix2Row + 3]) + column4
        newRow.extend([column1, column2, column3, column4])
        newMatrix.append(newRow)
    return newMatrix

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
                column1 = (Matrix[y][(x+i) % matrix2Col] * Matrix2[(x+i) % matrix2Col][matrix2Row]) + column1
            if matrix2RowLimit == 1:
                newMatrix.append(column1)
                break
            matrix2Row += 1
            newRow.append(column1)
            column1 = 0
        if matrix2RowLimit != 1:
            newMatrix.append(newRow)
    return newMatrix

#Multiplicacion entre una matrix y un vector
def multiVecMatrix(Vector, Matrix):
    matrix1Row = len(Matrix)
    matrixColumns = len(Matrix[0])
    newVector = []
    for y in range(matrix1Row):
        newNumber = 0
        vectorCol = 0
        for x in range(matrixColumns):
            newNumber = (Matrix[y][x] * Vector[vectorCol]) + newNumber
            vectorCol += 1
        newVector.append(newNumber)
    return(newVector)

#Crea matrices a partir de una lista
def createMatrix(row, col, listOfLists, multi = 1):
    matrix = []
    for i in range(row):
        
        rowList = []
        for j in range(col):
            
            # you need to increment through dataList here, like this:
            rowList.append((listOfLists[row * i + j]) * multi)    
                    
        matrix.append(rowList)
    
    return matrix

#Saca la trasnposicion de una matriz
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

#Obtiene la determinate de una matriz 3X3
def determinante3X3(matrix):
    rows = len(matrix)
    columns = len(matrix[0])
    newMatrix = []
    for y in range(rows):
        newRow = []
        for x in range(columns):
            if x == 2:
                newRow.extend([matrix[y][x], matrix[y][(x + 1) % columns], matrix[y][(x + 2) % columns]])
                break
            newRow.append(matrix[y][x])
        newMatrix.append(newRow)
    diagonal1 = 0
    diagonal2 = 0
    for x in range(columns):
        diagonal1 = (newMatrix[0][x] * newMatrix[1][x+1] * newMatrix[2][x+2]) + diagonal1
        diagonal2 = -(newMatrix[0][x+2] * newMatrix[1][x+1] * newMatrix[2][x]) + diagonal2
    determinante = diagonal1 + diagonal2
    return determinante

#Obtiene la inversa de una matriz 4X4
def inversa4X4(Matrix):
    newMatrix = transpose(Matrix)
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
                        verificador = True
                        rowCo.append(newMatrix[i][k])
                        if y == 0:
                            rowDe.append(Matrix[i][k])
                if verificador:
                    if y == 0:
                        detM.append(rowDe)
                    cofactorM.append(rowCo)
                    verificador = False
            deter = ((-1) ** exponentT) * determinante3X3(cofactorM)
            cofactorList.append(deter)
            if y == 0: 
               deter2 = ((-1) ** exponentT) * determinante3X3(detM)
               determinant = (Matrix[y][x] * deter2) + determinant
    Inverse = createMatrix(4, 4, cofactorList, (1/determinant))
    return Inverse