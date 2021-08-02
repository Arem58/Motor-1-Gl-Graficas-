import collections
import struct
from collections import namedtuple
from obj import Obj

V2 = namedtuple('Point2', ['x', 'y'])

def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # 2 bytes 
    return struct.pack('=h', w)

def dword(d):
    # 4 bytes
    return struct.pack('=l', d)

def color(r, g, b):
    # Acepta valores de 0 a 1
    return bytes( [int(b * 255), int(g * 255), int(r * 255)] )

Black = color(0,0,0)
White = color(1,1,1)

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
        self.clear_color = color(r, g, b)
    
    def glClear(self):
        #Crea una lista 2D de pixeles y a cada valor le asigna 3 bytes de color
        self.pixels = [[ self.clear_color for y in range(self.height)] for x in range(self.width)]

    def glColor(self, r, g, b):
        self.curr_color = color(r, g, b)
    
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
            self.fillPol(xMin, xMax, yMin, yMax, color(1, 1, 1), fill)

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
    
    def glLoadModel(self, filename, translate = V2(0.0, 0.0), scale = V2(1.0,1.0)):
        model = Obj(filename)

        for face in model.faces:
            vertCount = len(face)
            for v in range(vertCount):
                index0 =  face[v][0] - 1
                index1 =  face[(v + 1) % vertCount][0] - 1
                vert0 = model.vertices[index0]
                vert1 = model.vertices[index1]

                x0 = round(vert0[0] * scale.x + translate.x)
                y0 = round(vert0[1] * scale.y + translate.y)
                x1 = round(vert1[0] * scale.x + translate.x)
                y1 = round(vert1[1] * scale.x + translate.y)

                self.glLine(V2(x0, y0), V2(x1, y1), color(1,1,1))
    
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