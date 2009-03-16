from Blender import *
from PyPlasma import *
import Blender
import logging
import cStringIO

def stripIllegalChars(name):
    name=name.replace("*","_")
    name=name.replace("?","_")
    name=name.replace("\\","_")
    name=name.replace("/","_")
    name=name.replace("<","_")
    name=name.replace(">","_")
    name=name.replace(":","_")
    name=name.replace("\"","_")
    name=name.replace("|","_")
    name=name.replace("#","_")
    name=name.strip()
    return name

class blGMaterial:
    def __init__(self):
        pass
    
    def importObj(self, mat, rm):
        logging.info("[hsGMaterial::%s]" % (mat.key.name))
        
        try:
            m = Blender.Material.Get(mat.key.name[:20])
            return m
        except NameError:
            m = Blender.Material.New(mat.key.name[:20])
        
        m.mode = Material.Modes["VCOL_LIGHT"]
        
        i = 0
        
        for lkey in mat.layers:
            if lkey.type is plFactory.kLayer and lkey.object:
                lay = plLayer.Convert(lkey.object)
                blL = blLayer()
                l = blL.importObj(lay, rm)
                
                mapping = Texture.TexCo['ORCO']
                
                if lay.UVWSrc & 0xFFFF:
                    mapping = Texture.TexCo['UV']
                
                m.setTexture(i, l, mapping, Texture.MapTo['COL'])
                
                mtex = m.textures[i]
                mtex.uvlayer = "UVLayer" + str(lay.UVWSrc & 0xFFFF)
                i += 1
        
        return m

class blLayer:
    def __init__(self):
        pass
    
    def importObj(self, layer, rm):
        logging.info("[plLayer::%s]" % (layer.key.name))
        
        try:
            l = Blender.Texture.Get(layer.key.name[:20])
            return l
        except NameError:
            l = Blender.Texture.New(layer.key.name[:20])
        
        if layer.texture is None:
            l.setType('None')
        elif layer.texture.type is plFactory.kMipmap and layer.texture.object:
            l.setType('Image')
            mip = plMipmap.Convert(layer.texture.object)
            blmm = blMipmap()
            l.image = blmm.importObj(mip, rm)
        elif layer.texture.type is plFactory.kCubicEnvironmap and layer.texture.object:
            l.setType('EnvMap')
        
        l.rgbCol = (layer.runtime.red, layer.runtime.green, layer.runtime.blue)
        
        return l

class blMipmap:
    def __init__(self):
        pass
    
    def importObj(self, mip, rm):
        logging.info("[plMipmap::%s]" % (mip.key.name))
        
        try:
            i = Blender.Image.Get(mip.key.name[:20])
            return i
        except NameError:
            imgname = Blender.Get('tempdir') + stripIllegalChars(mip.key.name)
            fs = hsFileStream()
            fs.open(imgname, fmCreate)
            mip.writeToStream(fs)
            fs.close()
            i = Blender.Image.Load(imgname)
        i.pack()
        

        return i
