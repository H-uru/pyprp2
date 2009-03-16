from PyPlasma import *
from PyPRP_Node import *
from PyPRP_Surface import *
import os
import Blender

version = pvPots

def ExportMain(filename):
    scenes = Blender.Scene.Get()
    path, file = os.path.split(filename)
    agename = file[:len(file)-4]
    e = "Error: Need to specify a .age filename."
    if file[len(file)-4:] != ".age":
        raise e
    print path
    print file
    print agename
    
    rm = plResManager(version)    
##    age = plAgeInfo().addPage('')
    for i in range(len(scenes)):
        scn = scenes[i]
        loc = plLocation()
        loc.page = 0
        loc.prefix = i
        
        if version == pvEoa:
            pageName = '%s_%s' % (agename,scn.name)
        else:
            pageName = '%s_District_%s' % (agename,scn.name)

        #all materials exported
        for blMat in Material.Get():
            bmat = blGMaterial()
            bmat.Export(rm,loc,blMat)

        #then do the tree-export thing
        node = blSceneNode()
        node.Export(rm,loc,scn)

        page = plPageInfo()
        page.location = loc
        page.age = agename
        page.page = scn.name
        rm.AddPage(page)
        print rm.getKeys(loc,0)
        rm.WritePage(os.path.join(path,pageName)+'.prp', page)

