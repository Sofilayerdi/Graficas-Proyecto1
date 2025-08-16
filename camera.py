from MathLib import *

class Camera(object):
    def __init__(self):
        self.translation = [0, 0, 0]
        self.rotation = [0, 0, 0]  

    def GetCameraMatrix(self):
        rotateMat = RotationMatrix(self.rotation[0],
                                   self.rotation[1],
                                   self.rotation[2])
        
        translateMat = TranslationMatrix(self.translation[0],
                                         self.translation[1],
                                         self.translation[2])
        
        
        return translateMat * rotateMat


    def GetViewMatrix(self):
        
        return np.linalg.inv(self.GetCameraMatrix())  

        