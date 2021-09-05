from mathLib import *
from gl import SetColor
import random

def flat(render, **kwargs):
    A, B, C = kwargs['verts']
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['textCoords']
    normal = kwargs['normal']
    b, g, r = kwargs['color']

    b/= 255
    g/= 255
    r/= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tx, ty)

        b *= texColor[0]/255
        g *= texColor[1]/255
        r *= texColor[2]/255

    intensity = dot(normal, render.directional_light)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else: 
        return 0,0,0

def gourad(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b/= 255
    g/= 255
    r/= 255

    intensityA = dot(nA, render.directional_light)
    intensityB = dot(nB, render.directional_light)
    intensityC = dot(nC, render.directional_light)

    intensity = intensityA *u + intensityB *v + intensityC *w
    b*= intensity
    g*= intensity
    r*= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def phong(render, **kwargs):
    #Iluminacion por pixel
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['textCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b/= 255
    g/= 255
    r/= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tx, ty)

        b *= texColor[0]/255
        g *= texColor[1]/255
        r *= texColor[2]/255

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w

    normal = V3(nX, nY, nZ)

    intensity = dot(normal, render.directional_light)
    b*= intensity
    g*= intensity
    r*= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def unlit(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['textCoords']
    b, g, r = kwargs['color']

    b/= 255
    g/= 255
    r/= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    return r, g, b

def toon(render, **kwargs):
    #Iluminacion por pixel
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['textCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b/= 255
    g/= 255
    r/= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tx, ty)

        b *= texColor[0]/255
        g *= texColor[1]/255
        r *= texColor[2]/255

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w

    normal = V3(nX, nY, nZ)

    intensity = dot(normal, render.directional_light)

    #if intensity>0.85:
    #    intensity = 1
    #elif intensity>0.6:
    #    intensity = 0.8
    #elif intensity>0.45:
    #    intensity = 0.55
    #elif intensity>0.3:
    #    intensity = 0.4
    #elif intensity > 0.15:
    #    intensity = 0.25
    #else:
    #    intensity = 0.1

    if intensity > 0.7:
        intensity = 1
    elif intensity > 0.3:
        intensity = 0.5
    else:
        intensity = 0.05

    b*= intensity
    g*= intensity
    r*= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def sombreadoCool(render, **kwargs):
    #Iluminacion por pixel
    u, v, w = kwargs['baryCoords']
    nA, nB, nC = kwargs['normals']

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w

    normal = V3(nX, nY, nZ)

    intensity = dot(normal, render.directional_light)

    r,g,b = (0,0,0)

    if intensity>0.7:
        r = 1
    elif intensity>0.3:
        r = 0.5
        b = 0.5
    else:
        b = 1

    return r, g, b

def negative(render, **kwargs):
    #Iluminacion por pixel
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['textCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b/= 255
    g/= 255
    r/= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tx, ty)

        b *= texColor[0]/255
        g *= texColor[1]/255
        r *= texColor[2]/255

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w

    normal = V3(nX, nY, nZ)

    intensity = dot(normal, render.directional_light)
    b*= intensity
    g*= intensity
    r*= intensity

    b = 1 - b
    g = 1 - g
    r = 1 - r

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def wireframe(render, **kwargs):
   #Iluminacion por pixel
    u, v, w = kwargs['baryCoords']
    current = kwargs['currentColor']

    newColor = SetColor(1,1,1)

    r,g,b = (0,0,0)

    if newColor == current:
        r = 1
        g = 1
        b = 1
    else:
        if u < 0.05: 
            r,g,b = (1,1,1)
        elif v < 0.05:
            r,g,b = (1,1,1) 
        elif w < 0.05:
            r,g,b = (1,1,1) 

    return r, g, b

def VectorsColors(render, **kwargs):
   #Iluminacion por pixel
    u, v, w = kwargs['baryCoords']

    r,g,b = (0,0,0)

    if u < 0.05: 
        r,g,b = (1,1,1)
    elif v < 0.05:
        r,g,b = (1,1,1) 
    elif w < 0.05:
        r,g,b = (1,1,1) 
    else:
        r = u
        g = v
        b = w

    return r, g, b

def gradientH(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    x0, x1, y0, y1 = kwargs['globales']
    x, y = kwargs['locales']
    nA, nB, nC = kwargs['normals']

    mitad = x1 - x0
    margen = mitad * 0.01
    mitad = x1 - mitad/2

    r,g,b = (0,0,0)
    color1 = (0, 1, 1)
    color2 = (1, 0, 1)

    if x < mitad - margen:     
        r, g, b = (color1[0], color1[1], color1[2])
    elif x > mitad + margen: 
        r, g, b = (color2[0], color2[1], color2[2])
    else: 
        r,g,b =  ((color1[0] + color2[0])/2, (color1[1] + color2[1])/2, (color1[2] + color2[2])/2)
    
    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w
    
    normal = V3(nX, nY, nZ)

    intensity = dot(normal, render.directional_light)
    b*= intensity
    g*= intensity
    r*= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def gradientV(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    x0, x1, y0, y1 = kwargs['globales']
    x, y = kwargs['locales']
    nA, nB, nC = kwargs['normals']

    mitad = y1 - y0
    margen = mitad * 0.02
    margen2 = mitad * 0.01
    margen3 = mitad * 0.005
    mitad = y1 - mitad/2

    r,g,b = (0,0,0)
    color2 = (255/255, 30/255, 7/2550)
    color1 = (255/255, 243/255, 79/255)
    color3 = ((color1[0] + color2[0])/2, (color1[1] + color2[1])/2, (color1[2] + color2[2])/2)
    color4 = ((color1[0] + color3[0])/2, (color1[1] + color3[1])/2, (color1[2] + color3[2])/2)
    color5 = ((color3[0] + color2[0])/2, (color3[1] + color2[1])/2, (color3[2] + color2[2])/2)

    if y < mitad - margen - margen2 - margen3:
        r, g, b = (color1[0], color1[1], color1[2])
    elif y > mitad + margen + margen2 + margen3: 
        r, g, b = (color2[0], color2[1], color2[2])
    elif y < mitad - margen - margen2:
        r, g, b = (color4[0], color4[1], color4[2])   
    elif y > mitad + margen + margen2: 
        r, g, b = (color5[0], color5[1], color5[2])
    elif y < mitad - margen:
        r, g, b = (color3[0], color3[1], color3[2]) 
    elif y > mitad + margen: 
        r, g, b = (color3[0], color3[1], color3[2]) 
    else: 
        r,g,b =  ((color4[0] + color5[0])/2, (color4[1] + color5[1])/2, (color4[2] + color5[2])/2)

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w
    
    normal = V3(nX, nY, nZ)

    intensity = dot(normal, render.directional_light)
    b*= intensity
    g*= intensity
    r*= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

    return r, g, b

def thermal(render, **kwargs):
    #Iluminacion por pixel
    u, v, w = kwargs['baryCoords']
    nA, nB, nC = kwargs['normals']

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w

    normal = V3(nX, nY, nZ)

    intensity = dot(normal, render.directional_light)

    r,g,b = (0,0,0)

    if intensity>0.89:
        r = 252/255
        g = 249/255
        b = 141/255
    elif intensity>0.78:
        r = 255/255
        g = 228/255
        b = 47/255
    elif intensity>0.67:
        r = 255/255
        g = 188/255
        b = 0
    elif intensity>0.56:
        r = 255/255
        g = 147/255
        b = 3/255
    elif intensity>0.45:
        r = 251/255
        g = 108/255
        b = 35/255
    elif intensity>0.34:
        r = 237/255
        g = 80/255
        b = 67/255
    elif intensity>0.23:
        r = 148/255
        g = 3/255
        b = 166/255
    elif intensity>0.12:
        r = 206/255
        g = 38/255
        b = 122/255
    elif intensity>0.01:
        r = 0
        g = 6/255
        b = 75/255
    else:
        r = 78/255
        g = 0
        b = 151/255

    return r, g, b

def combinacionDeShaders(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    x0, x1, y0, y1 = kwargs['globales']
    x, y = kwargs['locales']
    nA, nB, nC = kwargs['normals']

    mitad = x1 - x0
    margen = mitad * 0.03
    mitad = x1 - mitad/2

    r,g,b = (0,0,0)
    color1 = (0, 1, 1)
    color2 = (1, 0, 1)

    if x < mitad - margen:
        if u < 0.05: 
            r,g,b = (1,1,1)
        elif v < 0.05:
            r,g,b = (1,1,1) 
        elif w < 0.05:
            r,g,b = (1,1,1) 
        else:
            r, g, b = (color1[0], color1[1], color1[2])
    elif x > mitad + margen: 
        if u < 0.05: 
            r,g,b = (1,1,1)
        elif v < 0.05:
            r,g,b = (1,1,1) 
        elif w < 0.05:
            r,g,b = (1,1,1) 
        else:
            r, g, b = (color2[0], color2[1], color2[2])
    else: 
        if u < 0.05: 
            r,g,b = (1,1,1)
        elif v < 0.05:
            r,g,b = (1,1,1) 
        elif w < 0.05:
            r,g,b = (1,1,1) 
        else:
            r,g,b =  ((color1[0] + color2[0])/2, (color1[1] + color2[1])/2, (color1[2] + color2[2])/2)
    
    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w
    
    normal = V3(nX, nY, nZ)

    intensity = dot(normal, render.directional_light)
    b*= intensity
    g*= intensity
    r*= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def textureBlend(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['textCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b/= 255
    g/= 255
    r/= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w

    normal = V3(nX, nY, nZ)

    intensity = dot(normal, render.directional_light)

    if intensity < 0:
        intensity = 0

    b*= intensity
    g*= intensity
    r*= intensity

    if render.active_texture2:
        texColor = render.active_texture2.getColor(tx, ty)
        b += (texColor[0] / 255) * (1 - intensity)
        g += (texColor[1] / 255) * (1 - intensity)
        r += (texColor[2] / 255) * (1 - intensity)


    return r, g, b

def normalMap(render, **kwargs):
    A, B, C = kwargs['verts']
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['textCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b/= 255
    g/= 255
    r/= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tx, ty)

        b *= texColor[0]/255
        g *= texColor[1]/255
        r *= texColor[2]/255

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w

    normal = V3(nX, nY, nZ)

    if render.normal_map:
        texNormal = render.normal_map.getColor(tx, ty)
        texNormal = V3((texNormal[2]/255) * 2 - 1, 
                       (texNormal[1]/255) * 2 - 1, 
                       (texNormal[0]/255) * 2 - 1)

        edge1 = sub(B, A)
        edge2 = sub(C, A)
        tA = V3(tA[0], tA[1], tA[2])
        tB = V3(tB[0], tB[1], tB[2])
        tC = V3(tC[0], tC[1], tC[2])
        deltaUV1 = sub(tB, tA)
        deltaUV2 = sub(tC, tA)

        try:
            f = 1 / (deltaUV1[0] * deltaUV2[1] - deltaUV2[0] * deltaUV1[1])
        except:
            f = 0.00000000000000000001

        tangente = V3(f * (deltaUV2[1] * edge1[0] - deltaUV1[1] * edge2[0]),
                      f * (deltaUV2[1] * edge1[1] - deltaUV1[1] * edge2[1]),
                      f * (deltaUV2[1] * edge1[2] - deltaUV1[1] * edge2[2]))

        bitangent = cross(normal, tangente)

        tangentMatrix = [[tangente[0],bitangent[0],normal[0]], 
                         [tangente[1],bitangent[1],normal[1]], 
                         [tangente[2],bitangent[2],normal[2]]]
        dirLight = V3(render.directional_light[0], render.directional_light[1], render.directional_light[2])
        dirLight = multiVecMatrix(dirLight, tangentMatrix)
        dirLight = norm(V3(dirLight[0], dirLight[1], dirLight[2]))

        intensity = dot(texNormal, dirLight)

    else: 
        intensity = dot(normal, render.directional_light)
    
    b*= intensity
    g*= intensity
    r*= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

