from Blender import *
from PyPlasma import *
import Blender
import logging

class blPhysical:
    def __init__(self):
        pass
    
    def importObj(self, obj, rm, col):
        logging.info("[plPhysical::%s]" % (obj.key.name))
        
        if col:
            data = Blender.Mesh.New("Col" + obj.key.name)
        else:
            data = Blender.Mesh.New(obj.key.name)
        
        data.verts.extend([Mathutils.Vector(v.X,v.Y,v.Z) for v in obj.verts])
        
        if obj.boundsType is plSimDefs.kProxyBounds:
            j = 0
            data.faces.extend([[obj.indices[(j*3)+c] for c in range(3)] for j in range(len(obj.indices) / 3)], indexList=True)
        
        return data
