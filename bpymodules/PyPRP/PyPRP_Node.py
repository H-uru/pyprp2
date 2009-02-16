from PyPlasma import *
from PyPRP_Object_Classes import *
from PyPRP_Misc import *
import Blender
import logging

class blSceneNode:
    def __init__(self):
        pass
    
    def Export(self,rm,loc,scn):
        node = plSceneNode(scn.name)
        rm.AddObject(loc,node)
        for blObj in scn.objects:
            blSceneObj = blSceneObject()
            node.addSceneObject(blSceneObj.Export(rm,loc,blObj).key)
        return node

    def importObj(self, node, rm, page, scn, globalScn):
        logging.info("[plSceneNode::%s]" % (node.key.name))
        
        for soref in node.sceneObjects:
            obj = plSceneObject.Convert(soref.object)
            sobj = blSceneObject()
            blObj = sobj.importObj(obj, rm, scn)
                
            try:
                globalScn.objects.link(blObj)
            except:
                logger.error("Unable to link object to global scene!")
