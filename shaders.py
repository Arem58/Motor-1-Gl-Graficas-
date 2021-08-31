from mathLib import *

def flat(render, **kwargs):
    A, B, C = kwargs['verts']
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

        b *= texColor[0]/255
        g *= texColor[1]/255
        r *= texColor[2]/255

    normal = norm(cross(sub(B,A), sub(C,A)))
    intensity = dot(normal, render.directional_light)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else: 
        return 0,0,0


def gourad(render, **kwargs):
    A, B, C = kwargs['verts']
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['textCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b/= 255
    g/= 255
    r/= 255

    intensityA = dot(nA, render.directional_light)
    intensityB = dot(nB, render.directional_light)
    intensityC = dot(nC, render.directional_light)

    colorA = (r * intensityA, g * intensityA, b * intensityA)
    colorB = (r * intensityB, g * intensityB, b * intensityB)
    colorC = (r * intensityC, g * intensityC, b * intensityC)

    r = colorA[0] * u + colorB[0] * v +colorC[0] * w
    g = colorA[1] * u + colorB[1] * v +colorC[1] * w
    b = colorA[2] * u + colorB[2] * v +colorC[2] * w

    r = 0 if r < 0 else r
    g = 0 if g < 0 else g
    b = 0 if b < 0 else b

    return r, g, b




