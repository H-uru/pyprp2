from PyPlasma import *
from PyPRP_Object_Classes import *
from PyPRP_Misc import *
import Blender
import logging

class blSceneNode:
    def __init__(self):
        pass
    
    def Export(self,rm,loc,scn,nodeName):
        node = plSceneNode(nodeName)
        for object in scn.objects:
            blSceneObj = blSceneObject()
            node.addSceneObject(blSceneObj.Export(rm,loc,node,object).key)
        rm.AddObject(loc,node)
        return node

    def importObj(self, node, rm, page):
        logging.info("[plSceneNode::%s]" % (node.key.name))
        
        for soref in node.sceneObjects:
            obj = plSceneObject.Convert(soref.object)
            sobj = blSceneObject()
            blObj = sobj.importObj(obj, rm, Blender.Scene.Get(page.page[:20]))
            #bobj = sobj.Import(rm, obj, Blender.Scene.Get(page.page[:20]))
                
            try:
                Blender.Scene.Get('_GLOBAL__AGE').objects.link(blObj)
            except:
                logger.error("Unable to link object to global scene!")
