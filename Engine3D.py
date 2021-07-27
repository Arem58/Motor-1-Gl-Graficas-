from gl import Renderer, V2, color

width = 52
height = 52

rend = Renderer(width, height)

#pol2 = [(321, 335), (288, 286), (339, 251), (374, 302)]

#rend.loadpol(pol2)


rend.glLine(V2(10, 10), V2(10, 40))
rend.glLine(V2(40, 10), V2(40, 40))
rend.fillPol(color(0, 0, 0), color(1, 1, 1), color(0, 1, 0), 40)

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