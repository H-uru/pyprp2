from PyPlasma import *
from PyPRP_Node import *
from PyPRP_Misc import *
import Blender
import time
import sys
import os
import logging

def importFile(path, debug=True):
    rm = plResManager()
    Blender.Text.New("AlcScript")
    parts = os.path.splitext(path)
    if debug:
        logging.basicConfig(level=logging.DEBUG,format='%(name)-12s %(levelname)-8s %(message)s',datefmt='',filename=parts[0]+'.log',filemode='w')
    else:
        logging.basicConfig(level=logging.INFO,format='%(name)-12s %(levelname)-8s %(message)s',datefmt='',filename=parts[0]+'.log',filemode='w')
    if parts[1] == '.age':
        age = rm.ReadAge(path, True)
        globalScn = None
        for s in Blender.Scene.Get():
            if s.getName() == '__GLOBAL':
                globalScn = s
        if globalScn is None:
            globalScn = Blender.Scene.New('__GLOBAL')
        pages = age.getNumPages()
        i = 0
        while i < pages:
            page = rm.FindPage(age.getPageLoc(i,rm.getVer()))
            importPrp(rm, page, globalScn)
            i += 1
    elif parts[1] == '.prp':
        page = rm.ReadPage(path)
        globalScn = None
        for s in Blender.Scene.Get():
            if s.getName() == '__GLOBAL':
                globalScn = s
        if globalScn is None:
            globalScn = Blender.Scene.New('__GLOBAL')
        importPrp(rm, page, globalScn)
    else:
        raise IOError("Could not load specified file %s" % (path))
    
    globalScn.makeCurrent()
    Blender.Window.QRedrawAll()

def importPrp(rm, page, globalScn):
    logging.getLogger().name = page.age+'.'+page.page
    start=time.clock()

    node = rm.getSceneNode(page.location)
    if node is None:
        return
    logging.info("Importing %s::%s" % (page.age, page.page))
    scn = None
    for s in Blender.Scene.Get():
        if s.getName() == page.page[:20]:
            scn = s
    if scn is None:
        scn = Blender.Scene.New(page.page[:20])
        logging.debug("Creating Blender scene %s" % (page.page[:20]))
    scn.makeCurrent()
    scnNode = blSceneNode()
    scnNode.importObj(node, rm, page, scn, globalScn)
    stop=time.clock()
    
    logging.info("Done in %.2f seconds" % (stop-start))
