#Carga un archivo obj

class Obj(object):
    def __init__(self, filename):

        with open(filename) as file:
            self.lines = file.read().splitlines

        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []
        self.read()

    def read(self): 
        for line in self.lines:
            if line:
                prefix, value = line.split(' ', 1)

                if prefix == 'v': #Vertices
                    self.vertices.append(map(list(float, value.split(' '))))
                elif prefix == ' vt': #Texture Coordinates
                    self.texcoords.append(value)
                elif prefix == 'vn': #Normales
                    self.normals.append(map(list(float, value.split(' '))))
                elif prefix == 'f': #Caras
                    self.faces.append( [ list(map(int, vert.split('/'))) for vert in value.split(' ') ] )


