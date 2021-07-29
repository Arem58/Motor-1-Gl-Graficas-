from gl import Renderer, V2, color

width = 1920
height = 1080

rend = Renderer(width, height)

rend.glLoadModel("estufa.obj",V2(width/2, height/2-100), V2(300, 300))

#pol1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330) ,(230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
#pol2 = [(321, 335), (288, 286), (339, 251), (374, 302)]
#pol3 = [(377, 249) ,(411, 197), (436, 249)] 
#pol4=[(413, 177) ,(448, 159) ,(502, 88) ,(553, 53), (535, 36) ,(676, 37) ,(660, 52),
#(750, 145) ,(761, 179) ,(672, 192) ,(659, 214) ,(615, 214) ,(632, 230) ,(580, 230),
#(597, 215) ,(552, 214) ,(517, 144) ,(466, 180)]

#rend.loadpol(pol1)
#rend.loadpol(pol2)
#rend.loadpol(pol3)
#rend.loadpol(pol4)


#rend.glLine(V2(10, 10), V2(10, 40))
#rend.glLine(V2(40, 10), V2(40, 40))
#rend.fillPol(color(0, 0, 0), color(1, 1, 1), color(0, 1, 0), 40)

#Triangle
#rend.glLine(V2(50, 50), V2(500, 400))
#rend.glLine(V2(910, 50), V2(500, 400))
#rend.glLine(V2(50, 50), V2(910, 50))

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