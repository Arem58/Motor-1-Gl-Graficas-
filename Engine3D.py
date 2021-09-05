from numpy.lib.type_check import imag
from gl import Renderer, V2, V3, SetColor
from shaders import *

from obj import Texture

width = 1920
height = 1080

rend = Renderer(width, height)

#rend.active_shader = flat

rend.active_texture = Texture("modelos/model.bmp")
rend.normal_map = Texture("modelos/model_normal.bmp")
#rend.active_texture2 = Texture("modelos/earthNight.bmp")

modelPosition = V3(0, 0, -10)
rend.directional_light = V3(0,0,1)

#-------------------------------------------------------------------------------------------------------------------------
#Shaders

rend.glLookAt(modelPosition, V3(0, 0, 0))

rend.active_shader = normalMap
rend.glLoadModel("modelos/model.obj",
                 translate = V3(-3, 0, -10),
                 scale = V3(3,3,3))

rend.active_shader = phong
rend.glLoadModel("modelos/model.obj",
                 translate = V3(3, 0, -10),
                 scale = V3(3,3,3))
#rend.active_shader = phong
#
#rend.glLoadModel("modelos/cube.obj", 
#                  translate = V3(3, 0, -10), 
#                  scale = V3(3, 3, 3), 
#                  rotate = V3(0, 0, 0))

#--------------------------------------------------------------------------------------------------------------------------

#SR5: Transformations

#Medium shot
#rend.glLookAt(modelPosition, V3(3, 1, 1))

#Low angle
#rend.glLookAt(modelPosition, V3(0, 3, -5))

#High angle
#rend.glLookAt(modelPosition, V3(0, -3, -5))
#rend.glLoadModel("cube.obj", 
#                  translate = modelPosition, 
#                  scale = V3(3, 3, 3), 
#                  rotate = V3(0 ,0 ,0))

#The Dutch Angle
#rend.glLookAt(modelPosition, V3(-8, 2, -7))
#rend.glLoadModel("cube.obj", modelTexture, modelPosition, V3(3, 3, 3), V3(0,-20,-20))

#--------------------------------------------------------------------------------------------------------------------------

#rend.glTriangle_bc(V2(10, 10), V2(190, 10), V2(100, 190))

#rend.glTriangle(V2(10, 70), V2(50, 160), V2(70, 80))
#rend.glTriangle(V2(180, 50), V2(150, 1), V2(70, 180))
#rend.glTriangle(V2(180, 150), V2(120, 160), V2(130, 180))

#rend.glViewMatrix(V3(100,50,0))

#pol1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330) ,(230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
#pol2 = [(321, 335), (288, 286), (339, 251), (374, 302)]
#pol3 = [(377, 249) ,(411, 197), (436, 249)] 
#pol4=[(413, 177) ,(448, 159) ,(502, 88) ,(553, 53), (535, 36) ,(676, 37) ,(660, 52),
#(750, 145) ,(761, 179) ,(672, 192) ,(659, 214) ,(615, 214) ,(632, 230) ,(580, 230),
#(597, 215) ,(552, 214) ,(517, 144) ,(466, 180)]
#pol5= [(682, 175) ,(708, 120), (735, 148), (739, 170)]

#rend.loadpol(pol1, True, color(0,1,0))
#rend.loadpol(pol2, True, color(0,1,0))
#rend.loadpol(pol4, True, color(0,1,0))
#rend.loadpol(pol5, True, color(0,0,0))
#rend.loadpol(pol3, True, color(0,1,0))

#rend.glLine(V2(20, 30), V2(25, 40))
#rend.glLine(V2(20, 30), V2(10, 28))
#rend.glLine(V2(20, 25), V2(10, 28))
#rend.glLine(V2(20, 25), V2(15, 17))
#rend.glLine(V2(25, 22), V2(15, 17))
#
#rend.glLine(V2(25, 40), V2(30, 30))
#rend.glLine(V2(30, 30), V2(40, 28))
#rend.glLine(V2(30, 25), V2(40, 28))
#rend.glLine(V2(30, 25), V2(35, 17))
#rend.glLine(V2(25, 22), V2(35, 17))

#rend.glLine(V2(10, 10), V2(10, 40))
#rend.glLine(V2(15, 10), V2(15, 40))
#rend.glLine(V2(20, 10), V2(20, 40))
#rend.glLine(V2(25, 10), V2(25, 40))
#rend.glLine(V2(40, 10), V2(40, 40))
#rend.glLine(V2(35, 10), V2(35, 40))
#rend.glLine(V2(30, 10), V2(30, 40))


#rend.glLine(V2(10, 10), V2(15, 10))
#rend.glLine(V2(20, 10), V2(25, 10))
#rend.glLine(V2(30, 10), V2(35, 10))

#rend.glLine(V2(10, 40), V2(15, 40))
#rend.glLine(V2(20, 40), V2(25, 40))
#rend.glLine(V2(30, 40), V2(35, 40))
#rend.fillPol(color(1, 1, 1), color(0, 1, 0), 165, 250, 330, 410)



#Triangle
#rend.glLine(V2(50, 50), V2(500, 400))
#rend.glLine(V2(910, 50), V2(500, 400))
#rend.glLine(V2(50, 50), V2(910, 50))
#
#u, v, w = baryCoords(V2(50, 50),  V2(500, 400), V2(910, 50), V2(430, 50))
#print(u,v,w)

#square
#rend.glLine(V2(50, 50), V2(910, 50))
#rend.glLine(V2(50, 50), V2(50, 500))
#rend.glLine(V2(50, 500), V2(910, 500))
#rend.glLine(V2(910, 500), V2(910, 50))

#pentagon
#rend.glLine(V2(280, 520), V2(680, 520))
#rend.glLine(V2(180, 260), V2(280, 520))
#rend.glLine(V2(280, 20), V2(180, 260))
#rend.glLine(V2(680, 520), V2(780, 260))
#rend.glLine(V2(680, 20), V2(780, 260))
#rend.glLine(V2(280, 20), V2(680, 20))

#rhombus
#rend.glLine(V2(480, 520), V2(380, 260))
#rend.glLine(V2(480, 520), V2(580, 260))
#rend.glLine(V2(480, 20), V2(380, 260))
#rend.glLine(V2(480, 20), V2(580, 260))

#Star
#rend.glLine(V2(280, 20), V2(480, 520))
#rend.glLine(V2(680, 20), V2(480, 520))
#rend.glLine(V2(680, 20), V2(180, 360))
#rend.glLine(V2(280, 20), V2(780, 360))
#rend.glLine(V2(180, 360), V2(780, 360))


rend.glFinish("output.bmp")