import struct
from collections import namedtuple
from obj import Obj
import random
import numpy as np

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])

def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # 2 bytes 
    return struct.pack('=h', w)

def dword(d):
    # 4 bytes
    return struct.pack('=l', d)

def SetColor(r, g, b):
    # Acepta valores de 0 a 1
    return bytes( [int(b * 255), int(g * 255), int(r * 255)] )

def sub(v0, v1):
  
  return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def dot(v0, v1):
  
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

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

Black = SetColor(0,0,0)
White = SetColor(1,1,1)

class Renderer(object):
    def __init__(self, width, height):
        self.clear_color = Black
        self.curr_color = White
        self.glCreateWindow(width, height)

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()
        self.glViewport(0, 0, width, height)

    def glViewport(self, x, y, width, height):
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height

    def glVertex(self, x, y):
        Xw = round((x + 1) * (self.vpWidth * 0.5) + self.vpX)
        Yw = round((y + 1) * (self.vpHeight * 0.5) + self.vpY)
        if (Xw == self.vpWidth):
            Xw -= 1
        if (Yw == self.vpHeight):
            Yw -= 1
        #print(Xw, Yw)
        self.pixels[int(Xw)][int(Yw)] = self.curr_color

    def glClearColor(self, r, g, b):
        self.clear_color = SetColor(r, g, b)
    
    def glClear(self):
        #Crea una lista 2D de pixeles y a cada valor le asigna 3 bytes de color
        self.pixels = [[ self.clear_color for y in range(self.height)] for x in range(self.width)]

        self.zbuffer = [[ -float('inf') for y in range(self.height)] for x in range(self.width)]

    def glColor(self, r, g, b):
        self.curr_color = SetColor(r, g, b)
    
    def glPoint(self, x, y, color = None):
        if x < self.vpX or x >= self.vpX + self.vpWidth or y < self.vpY or y >= self.vpY + self.vpHeight:
            return
        if (0 < x < self.width) and (0 < y < self.height): 
            self.pixels[int(x)][int(y)] = color or self.curr_color

    def loadpol(self, pol, pintar, fill = None):
        xMin = 0
        xMax = 0
        yMin = 0
        yMax = 0
        lenPol = len(pol)

        for i in range(lenPol):
            x0 = pol[i][0]
            y0 = pol[i][1]
            x1 = pol[(i + 1) % lenPol][0]
            y1 = pol[(i + 1) % lenPol][1]
            if xMin == 0 and yMin == 0:
                xMin, yMin = x0, y0
            if (x0 < xMin):
                xMin = x0
            if (x1 > xMax):
                xMax = x1
            if (y0 < yMin):
                yMin = y0
            if (y1 > yMax):
                yMax = y1
            self.glLine(V2(x0, y0), V2(x1, y1))
        print(xMin, xMax, yMin, yMax)
        if pintar:
            self.fillPol(xMin, xMax, yMin, yMax, SetColor(1, 1, 1), fill)

    def fillPol(self, xMin, xMax, yMin, yMax, lineColor, fillColor = None ):
        for y in range(yMin, yMax):
            for x in range(xMin, xMax):
                if self.pixels[x][y] == lineColor:
                    if self.pixels[x + 1][y] != lineColor:
                        x += 1
                        x0 = x
                        #Revision horizontal
                        while x <= xMax:
                            #Si encontro pareja horizontal
                            if self.pixels[x][y] == lineColor:
                                if y not in [yMax, yMin]:
                                    verificador1 = False
                                    verificador2 = False
                                    revisando1 = True
                                    revisando2 = True
                                    pintar = False
                                    y1 = y2 = y 
                                    #Revision vertical para abajo
                                    while True:
                                        if y1 != yMin:
                                            y1 -= 1 
                                            if self.pixels[x0][y1] == lineColor:
                                                verificador1 = True
                                            if y1 == yMin:
                                                revisando1 = False

                                        if y2 != yMax:
                                            y2 += 1
                                            if self.pixels[x0][y2] == lineColor:
                                                verificador2 = True
                                            if y2 == yMax:
                                                revisando2 = False
                                        
                                        if verificador2 == True and verificador1 == True:
                                            pintar = True
                                            break
                                        else: 
                                            if y1 == yMin or y2 == yMax:
                                                if (verificador2 != True and revisando2 != True) or (verificador1 != True and revisando1 != True):
                                                    break 
                                    if pintar:
                                        #self.glPoint(x - 1, y, fillColor)
                                        #self.glPoint(x0, y, background)
                                        self.glLine(V2(x0, y), V2(x-1, y), fillColor)
                                break
                            x += 1
                            
    
    def glLine(self, v0, v1, color = None):
        x0 = v0.x
        x1 = v1.x
        y0 = v0.y
        y1 = v1.y

        if x0 == x1 and y0 == y1:
            self.glPoint(x0, y1, color)
            return

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx 

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        
        if (x0 > x1):
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        m = dy/dx
        offset = 0 
        limit = 0.5
        y = y0

        for x in range(x0, x1 + 1):
                if steep:
                    self.glPoint(y, x, color)
                else: 
                    self.glPoint(x, y, color)
                offset += m
                if offset >= limit:
                    y += 1 if y0 < y1 else -1
                    limit += 1
                
    def glLine_NDC(self, v0, v1, color = None):

        x0 = int( (v0.x + 1) * (self.vpWidth / 2) + self.vpX)
        x1 = int( (v1.x + 1) * (self.vpWidth / 2) + self.vpX)
        y0 = int( (v0.y + 1) * (self.vpHeight / 2) + self.vpY)
        y1 = int( (v1.y + 1) * (self.vpHeight / 2) + self.vpY)

        if x0 == x1 and y0 == y1:
            self.glPoint(x0, y1, color)
            return

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5
        m = dy/dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x, color)
            else:
                self.glPoint(x, y, color)

            offset += m
            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 1
    
    def glTransform(self, vertex, translate=V3(0,0,0), scale=V3(1,1,1)):
        return V3(vertex[0] * scale.x + translate.x,
                  vertex[1] * scale.y + translate.y,
                  vertex[2] * scale.z + translate.z)
    
    def glLoadModel(self, filename, texture = None, translate = V3(0.0, 0.0, 0.0), scale = V3(1.0, 1.0, 1.0)):
        model = Obj(filename)

        light = V3(0, 0, 1)

        for face in model.faces:
            vertCount = len(face)

            vert0 = model.vertices[face[0][0] - 1]
            vert1 = model.vertices[face[1][0] - 1]
            vert2 = model.vertices[face[2][0] - 1]

            vt0 = model.texcoords[face[0][1] - 1]
            vt1 = model.texcoords[face[1][1] - 1]
            vt2 = model.texcoords[face[2][1] - 1]

            a = self.glTransform(vert0, translate, scale)
            b = self.glTransform(vert1, translate, scale)
            c = self.glTransform(vert2, translate, scale)

            if vertCount == 4:
                vert3 = model.vertices[face[3][0] - 1]
                vt3 = model.texcoords[face[3][1] - 1]
                d = self.glTransform(vert3, translate, scale)

            _cor = SetColor(random.random(), random.random(), random.random())
            normal = norm(cross(sub(a, b), sub(b, c)))
            intensity = dot(normal, light)

            if intensity > 1:
                intensity = 1
            elif intensity < 0:
                intensity = 0
            
            self.glTriangle_bc(a, b, c, SetColor(intensity, intensity, intensity))

            if vertCount == 4:
                self.glTriangle_bc(a, c, d, SetColor(intensity, intensity, intensity)) 

            #x0 = round(vert0[0] * scale.x + translate.x)
    
    def glTriangle_standard(self, A, B, C, color = None):
        
        self.glLine(A, B, color)
        self.glLine(B, C, color)
        self.glLine(C, A, color)

        if A.y < B.y:
            A, B = B, A
        
        if A.y < C.y:
            A, C = C, A

        if B.y < C.y:
            B, C = C, B
        
        def flatBottomTriangle(v1, v2, v3):
            d_21 = (v2.x - v1.x) / (v2.y - v1.y)
            d_31 = (v3.x - v1.x) / (v3.y - v1.y)
            
            x1 = v2.x
            x2 = v3.x

            for y in range(v2.y, v1.y + 1):
                self.glLine(V2(int( x1), y), V2(int( x2), y), color)
                x1 += d_21
                x2 += d_31

        def flatTopTriangle(v1, v2, v3):
            d_31 = (v3.x - v1.x) / (v3.y - v1.y)
            d_32 = (v3.x - v2.x) / (v3.y - v2.y)

            x1 = v3.x
            x2 = v3.x 

            for y in range(v3.y, v1.y + 1):
                self.glLine(V2(int( x1), y), V2(int( x2), y), color)
                x1 += d_31
                x2 += d_32

        if B.y == C.y:
            #Triangulo con base inferior
            try:
                flatBottomTriangle(A, B, C)
            except:
                pass
        elif A.y == B.y:
            #Triangulo con base superior
            try:
                flatTopTriangle(A, B, C)
            except:
                pass
        else:
            #dividir el triangulo en dos
            #dibujar ambos casos
            #Teorema de intercepto
            try:
                D_x = A.x + ((B.y - A.y) / (C.y - A.y)) * (C.x - A.x)
                D = V2(D_x , B.y)
                flatBottomTriangle(A, B, D)
                flatTopTriangle(B, D, C)
            except:
                pass
           
    def glTriangle_bc(self, A, B, C, color = None):
        #Bounding Box
        minX = round(min(A.x, B.x, C.x))
        minY = round(min(A.y, B.y, C.y))
        maxX = round(max(A.x, B.x, C.x))
        maxY = round(max(A.y, B.y, C.y))
 
        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                u, v, w = baryCoords(A, B, C, V2(x, y))
                if u >= 0 and v >= 0 and w >= 0:
                    z = A.z * u + B.z * v + C.z * w

                    if z > self.zbuffer[x][y]:
                        self.glPoint(x, y, color)
                        self.zbuffer[x][y] = z





    def glFinish(self, filename):
        with open(filename, "wb") as file:
            # Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color Table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])