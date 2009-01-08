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
    parts = os.path.splitext(path)
    if debug:
        logging.basicConfig(level=logging.DEBUG,format='%(name)-12s %(levelname)-8s %(message)s',datefmt='',filename=parts[0]+'.log',filemode='w')
    else:
        logging.basicConfig(level=logging.INFO,format='%(name)-12s %(levelname)-8s %(message)s',datefmt='',filename=parts[0]+'.log',filemode='w')
    if parts[1] == '.age':
        age = rm.ReadAge(path, True)
        try:
            Blender.Scene.Get('_GLOBAL__AGE')
        except NameError:
            Blender.Scene.New('_GLOBAL__AGE')
        pages = age.getNumPages()
        i = 0
        while i < pages:
            page = rm.FindPage(age.getPageLoc(i,rm.getVer()))
            importPrp(rm, page)
            i += 1
    elif parts[1] == '.prp':
        page = rm.ReadPage(path)
        try:
            Blender.Scene.Get('_GLOBAL__AGE')
        except NameError:
            Blender.Scene.New('_GLOBAL__AGE')
        importPrp(rm, page)
    else:
        raise IOError("Could not load specified file %s" % (path))
    
    Blender.Scene.Get('_GLOBAL__AGE').makeCurrent()
    Blender.Window.QRedrawAll()

def importPrp(rm, page):
    logging.getLogger().name = page.age+'.'+page.page
    start=time.clock()

    node = rm.getSceneNode(page.location)
    if node is None:
        return
    logging.info("Importing %s::%s" % (page.age, page.page))
    try:
        scn = Blender.Scene.Get(page.page[:20])
    except NameError:
        scn = Blender.Scene.New(page.page[:20])
        logging.debug("Creating Blender scene %s" % (page.page[:20]))
    scn.makeCurrent()
    scnNode = blSceneNode()
    scnNode.importObj(node, rm, page)
    stop=time.clock()
    
    logging.info("Done in %.2f seconds" % (stop-start))
