from PyPlasma import *
from PyPRP_Node import *
import os
import Blender

def ExportMain(filename):
    filenameS = os.path.split(filename)
    path = filenameS[0]
    file = filenameS[1]
    agename = file[:len(file)-4]
    print path
    print file
    print agename
    rm = plResManager(pvPots)
    for i in range(len(Blender.Scene.Get())):
        scn = Blender.Scene.Get()[i]
        loc = plLocation()
        loc.prefix = 1
        loc.page = i

        print scn.name
        nodeName = '%s_District_%s' % (agename,scn.name)
        node = blSceneNode()
        node.Export(rm,loc,scn,nodeName)
        page = plPageInfo()
        page.location = loc
        page.age = agename
        page.page = scn.name
        rm.AddPage(page)
        rm.WritePage(os.path.join(path,nodeName)+'.prp', page)

