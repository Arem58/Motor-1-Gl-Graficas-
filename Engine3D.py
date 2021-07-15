from gl import Renderer

width = 960
height = 540

rend = Renderer(width, height)

rend.glPoint(400, 300)
rend.glViewport(0, 0, 960, 540)
rend.glVertex(-1, 1)
rend.glVertex(1, -1)
rend.glVertex(0, 0)
rend.glVertex(0, -1)
rend.glVertex(-1, 0)
rend.glVertex(1, 1)
rend.glVertex(0, 1)
rend.glVertex(1, 0)
rend.glVertex(-1, -1)
rend.glFinish("output.bmp")