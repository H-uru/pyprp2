from PyPlasma import *
import Blender

class blGMaterial():
    def __init__(self):
        pass
    def Export(self,rm,loc,blMat):
        gm = hsGMaterial(blMat.name)
        rm.AddObject(loc,gm)
        return gm
