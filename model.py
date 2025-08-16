from MathLib import *
from OBJLoader import *
from BMPTexture import BMPTexture


class Model(object):
    def __init__(self, filename):
        objFile = OBJ(filename)

        self.vertices = objFile.vertices
        self.normals = objFile.normals
        self.texCoords = objFile.texcoords
        self.faces = objFile.faces

        self.translation = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.scale = [1, 1, 1]

        self.vertexShader = None
        self.fragmentShader = None

        self.textureList = []

    def GetModelMatrix(self):
        translateMat = TranslationMatrix(self.translation[0],
                                         self.translation[1],
                                         self.translation[2])

        rotateMat = RotationMatrix(self.rotation[0],
                                   self.rotation[1],
                                   self.rotation[2])

        scaleMat = ScaleMatrix(self.scale[0],
                               self.scale[1],
                               self.scale[2])

        return translateMat * rotateMat * scaleMat
    
    def LoadTexture(self, filename):
        self.textureList.append(BMPTexture(filename))
