import struct
from collections import namedtuple
from obj import Obj
import random
import numpy as np
from math import cos, sin, tan
from mathLib import *

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])

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

Black = SetColor(0,0,0)
White = SetColor(1,1,1)

class Renderer(object):
    def __init__(self, width, height):
        self.clear_color = Black
        self.curr_color = White
        self.glViewMatrix()
        self.glCreateWindow(width, height)
        self.puntosGlobales = None

        self.background = None
        self.normal_map = None
        self.active_texture = None
        self.active_texture2 = None
        self.active_shader = None

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

        #self.viewPortMatrix = np.matrix([[width * 0.5,0,0,x + width*0.5],
        #                           [0,height * 0.5,0,y + height*0.5],
        #                           [0,0,0.5,0.5],
        #                           [0,0,0,1]])
        
        self.viewPortMatrix = [[width * 0.5,0,0,x + width*0.5],
                                [0,height * 0.5,0,y + height*0.5],
                                [0,0,0.5,0.5],
                                [0,0,0,1]]

        self.glProyectionMatrix()

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

        self.zbuffer = [[ float('inf')for y in range(self.height)] for x in range(self.width)]

    def glClearBackground(self):
        if self.background:
            for x in range(self.vpX, self.vpX + self.vpWidth):
                for y in range(self.vpY, self.vpY  + self.vpHeight):
                    
                    tx = (x - self.vpX)/self.vpWidth
                    ty = (y - self.vpY)/self.vpHeight

                    self.glPoint(x, y, self.background.getColor(tx, ty))

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
        #print(xMin, xMax, yMin, yMax)
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
    
    def glTransform(self, vertex, vMatrix):
        augVertex = V4(vertex[0], vertex[1], vertex[2], 1)
        #transVertex = vMatrix @ augVertex
        transVertex2 = multiVecMatrix(augVertex, vMatrix)

        #transVertex = transVertex.tolist()[0]

        transVertex2 = V3(transVertex2[0]/transVertex2[3], 
                         transVertex2[1]/transVertex2[3],   
                         transVertex2[2]/transVertex2[3])
       
        return transVertex2

    def glDirTransform(self, dirVector, vMatrix):
        augVertex = V4(dirVector[0], dirVector[1], dirVector[2], 0)
        #transVertex = vMatrix @ augVertex
        transVertex2 = multiVecMatrix(augVertex, vMatrix)

        #transVertex = transVertex.tolist()[0]

        transVertex2 = V3(transVertex2[0], 
                         transVertex2[1],   
                         transVertex2[2])
       
        return transVertex2

    def glCamTransform(self, vertex):
        augVertex = V4(vertex[0], vertex[1], vertex[2], 1)
        #transVertex = self.viewPortMatrix @ self.proyectionMatrix @ self.viewMatrix @ augVertex
        transVertex2 = multyMatrix(self.viewPortMatrix, self.proyectionMatrix)
        transVertex3 = multyMatrix(transVertex2, self.viewMatrix)
        transVertex4 = multiVecMatrix(augVertex ,transVertex3)

        #transVertex = transVertex.tolist()[0]
        #print(transVertex)
        #print(transVertex4)

        transVertex4 = V3(transVertex4[0]/transVertex4[3], 
                         transVertex4[1]/transVertex4[3],   
                         transVertex4[2]/transVertex4[3])
       
        return transVertex4

    def glCreateRotationMatrix(self, rotate=V3(0,0,0)):
        pitch = degreesRad(rotate.x)
        yaw = degreesRad(rotate.y)
        roll = degreesRad(rotate.z)

        #rotationX = np.matrix([[1,0,0,0],
        #                        [0,cos(pitch),-sin(pitch),0],
        #                        [0,sin(pitch),cos(pitch),0],
        #                        [0,0,0,1]])
        
        #rotationY = np.matrix([[cos(yaw),0,sin(yaw),0],
        #                        [0,1,0,0],
        #                        [-sin(yaw),0,cos(yaw),0],
        #                        [0,0,0,1]])

        #rotationZ = np.matrix([[cos(roll),-sin(roll),0,0],
        #                        [sin(roll),cos(roll),0,0],
        #                        [0,0,1,0],
        #                        [0,0,0,1]])
        
        rotationX2 = [[1,0,0,0],
                      [0,cos(pitch),-sin(pitch),0],
                      [0,sin(pitch),cos(pitch),0],
                      [0,0,0,1]]
        
        rotationY2 = [[cos(yaw),0,sin(yaw),0],
                      [0,1,0,0],
                      [-sin(yaw),0,cos(yaw),0],
                      [0,0,0,1]]

        rotationZ2 = [[cos(roll),-sin(roll),0,0],
                      [sin(roll),cos(roll),0,0],
                      [0,0,1,0],
                      [0,0,0,1]]

        newMatrix1 = multyMatrix(rotationX2, rotationY2)
        newMatrix2 = multyMatrix(newMatrix1, rotationZ2)

        return newMatrix2
    
    def glCreateObjectMatrix(self, translate = V3(0,0,0), scale = V3(1,1,1), rotate = V3(0,0,0)):
        #translateMatrix = np.matrix([[1,0,0,translate.x],
        #                            [0,1,0,translate.y],
        #                            [0,0,1,translate.z],
        #                            [0,0,0,1]])

        #scaleMatrix = np.matrix([[scale.x,0,0,0],
        #                         [0,scale.y,0,0],
        #                         [0,0,scale.z,0],
        #                         [0,0,0,1]])

        translateMatrix2 = [[1,0,0,translate.x],
                            [0,1,0,translate.y],
                            [0,0,1,translate.z],
                            [0,0,0,1]]

        scaleMatrix2 = [[scale.x,0,0,0],
                        [0,scale.y,0,0],
                        [0,0,scale.z,0],
                        [0,0,0,1]]
        
        rotationMatrix = self.glCreateRotationMatrix(rotate)

        newMatrix1 = multyMatrix(translateMatrix2, scaleMatrix2)
        newMatrix2 = multyMatrix(newMatrix1, rotationMatrix)

        return newMatrix2
    
    def glViewMatrix(self, translate = V3(0,0,0), rotate = V3(0,0,0)):
        self.camMatrix = self.glCreateObjectMatrix(translate, V3(1,1,1), rotate)
        #self.viewMatrix = np.linalg.inv(camMatrix)
        self.viewMatrix = inversa4X4(self.camMatrix)
        #print(self.viewMatrix)
        #print(self.viewMatrix2)

    def glLookAt(self, eye, camPos = V3(0,0,0)):
        forward = norm(sub(camPos, eye))
        right = norm(cross(V3(0,1,0), forward))
        up = norm(cross(forward, right))

        camMatrix = [[right[0],up[0],forward[0],camPos.x],
                     [right[1],up[1],forward[1],camPos.y],
                     [right[2],up[2],forward[2],camPos.z],
                     [0,0,0,1]]
        
        self.viewMatrix = inversa4X4(camMatrix)

    def glProyectionMatrix(self, n = 0.1, f = 1000, fov = 60):
        t = tan(degreesRad(fov)/2) * n
        r = t * self.vpWidth / self.vpHeight

        #self.proyectionMatrix = np.matrix([[n/r,0,0,0],
        #                                   [0,n/t,0,0],
        #                                   [0,0,-(f + n)/(f - n),-(2* f * n)/(f - n)],
        #                                   [0,0,-1,0],])

        self.proyectionMatrix = [[n/r,0,0,0],
                                  [0,n/t,0,0],
                                  [0,0,-(f + n)/(f - n),-(2* f * n)/(f - n)],
                                  [0,0,-1,0],]

    def glLoadModel(self, filename, translate = V3(0, 0, 0), scale = V3(1, 1, 1), rotate = V3(0,0,0)):
        model = Obj(filename)

        Ming = [model.xMin, model.yMin, 0]
        Maxg = [model.xMax, model.yMax, 0]

        modelMatrix = self.glCreateObjectMatrix(translate, scale, rotate)
        rotationMatrix = self.glCreateRotationMatrix(rotate)

        Ming = self.glTransform(Ming, modelMatrix)
        Maxg = self.glTransform(Maxg, modelMatrix)
        aMing = self.glCamTransform(Ming)
        bMaxg = self.glCamTransform(Maxg)

        self.puntosGlobales = [aMing.x, bMaxg.x, aMing.y, bMaxg.y]

        for face in model.faces:
            vertCount = len(face)

            vert0 = model.vertices[face[0][0] - 1]
            vert1 = model.vertices[face[1][0] - 1]
            vert2 = model.vertices[face[2][0] - 1]

            vt0 = model.texcoords[face[0][1] - 1]
            vt1 = model.texcoords[face[1][1] - 1]
            vt2 = model.texcoords[face[2][1] - 1]

            vn0 = model.normals[face[0][2] - 1]
            vn1 = model.normals[face[1][2] - 1]
            vn2 = model.normals[face[2][2] - 1]

            vn0 = self.glDirTransform(vn0, rotationMatrix)
            vn1 = self.glDirTransform(vn1, rotationMatrix)
            vn2 = self.glDirTransform(vn2, rotationMatrix)

            vert0 = self.glTransform(vert0, modelMatrix)
            vert1 = self.glTransform(vert1, modelMatrix)
            vert2 = self.glTransform(vert2, modelMatrix)

            if vertCount == 4:
                vert3 = model.vertices[face[3][0] - 1]
                vt3 = model.texcoords[face[3][1] - 1]
                vn3 = model.normals[face[3][2] - 1]
                vn3 = self.glDirTransform(vn3, rotationMatrix)
                vert3 = self.glTransform(vert3, modelMatrix)

            _cor = SetColor(random.random(), random.random(), random.random())
            #normal = norm(cross(sub(b, a), sub(c, a)))
            #intensity = dot(normal, self.directional_light)

            #normal = np.cross(np.subtract(vert1,vert0), np.subtract(vert2,vert0))
            #normal = normal / np.linalg.norm(normal) # la normalizamos
            #intensity = np.dot(normal, -light)

            #if intensity > 1:
            #    intensity = 1
            #elif intensity < 0:
            #    intensity = 0

            a = self.glCamTransform(vert0)
            b = self.glCamTransform(vert1)
            c = self.glCamTransform(vert2)
            if vertCount == 4:
                d = self.glCamTransform(vert3)

            self.glTriangle_bc(a, b, c, textCoords=(vt0, vt1, vt2), normals=(vn0, vn1, vn2),verts = (vert0, vert1, vert2))
            if vertCount == 4:
                self.glTriangle_bc(a, c, d, textCoords=(vt0, vt2, vt3), normals=(vn0, vn2, vn3), verts = (vert0, vert2, vert3)) 

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
           
    def glTriangle_bc(self, A, B, C, textCoords = (), normals = (), verts = (), color = None):
        #Bounding Box
        minX = round(min(A.x, B.x, C.x))
        minY = round(min(A.y, B.y, C.y))
        maxX = round(max(A.x, B.x, C.x))
        maxY = round(max(A.y, B.y, C.y))

        normal = norm(cross(sub(verts[1],verts[0]), sub(verts[2],verts[0])))
 
        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                u, v, w = baryCoords(A, B, C, V2(x, y))
                if u >= 0 and v >= 0 and w >= 0:
                    z = A.z * u + B.z * v + C.z * w
                    
                    if 0 <= x < self.width and 0 <= y < self.height:
                        if z < self.zbuffer[x][y] and z<=1 and z >= -1:

                            self.zbuffer[x][y] = z

                            currentColor = self.pixels[x][y]

                            locales = [x, y]

                            if self.active_shader:
                                r, g, b = self.active_shader(self, 
                                                             verts = verts,
                                                             baryCoords = (u, v, w), 
                                                             textCoords = textCoords, 
                                                             normals =  normals,
                                                             normal = normal,
                                                             globales = self.puntosGlobales, 
                                                             locales = locales, 
                                                             currentColor = currentColor,
                                                             color = color or self.curr_color)
                                self.glPoint(x,y, SetColor( r, g, b) )
                            else: 
                                self.glPoint(x,y, SetColor( r, g, b) or self.curr_color )





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