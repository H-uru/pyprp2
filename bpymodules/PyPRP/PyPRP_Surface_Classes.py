from PyPlasma import *
import Blender

class blGMaterial():
    def __init__(self):
        pass
    def Export(self,rm,loc,blMat):
        gm = hsGMaterial(blMat.name)
        for layer in blMat.getTextures():
            if layer != None:
                l = blLayer()
                gm.addLayer(l.Export(rm,loc,layer,blMat).key)
        rm.AddObject(loc,gm)
        return gm

class blLayer():
    def __init__(self):
        pass
    def Export(self,rm,loc,b_mtex,parent_blMat):
        plL = plLayer()
        if b_mtex != None:
            if parent_blMat.getRGBCol() == (1.0,1.0,1.0): #if the main mat color is white we can use the per-layer colors
                R_r = b_mtex.col[0]
                R_g = b_mtex.col[1]
                R_b = b_mtex.col[2]
                R_a = b_mtex.colfac
            else:
                R_r = parent_blMat.getRGBCol()[0]
                R_g = parent_blMat.getRGBCol()[1]
                R_b = parent_blMat.getRGBCol()[2]
                R_a = b_mtex.colfac
            plL.runtime = hsColorRGBA(R_r,R_g,R_b,R_a)
        else:
            print "NONETYPE!"
    #        if b_mtex.tex.type == Texture.Types.NONE:
    #        if blL.type == Texture.IMAGE:
        rm.AddObject(loc, plL)
        return plL