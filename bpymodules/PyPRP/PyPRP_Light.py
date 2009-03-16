from PyPlasma import *
import Blender
import logging

class blOmniLightInfo:
    def __init__(self):
        pass
   
    def importObj(self, li, rm):
        logging.info("[plOmniLightInfo::%s]" % (li.key.name))
       
        data = Blender.Lamp.New('Lamp', li.key.name)
       
        data.setDist(li.attenCutoff * 16)
        data.mode |= Blender.Lamp.Modes["Quad"]
       
        maxval = max(max(li.diffuse.red,li.diffuse.green),li.diffuse.blue)
       
        if maxval > 1:
            data.energy = maxval * 0.5
            data.R = li.diffuse.red / maxval
            data.G = li.diffuse.green / maxval
            data.B = li.diffuse.blue / maxval
        else:
            data.energy = 1 * 0.5
            data.R = li.diffuse.red
            data.G = li.diffuse.green
            data.B = li.diffuse.blue
       
        return data
   
