#    This file is part of PyPRP2.
#    
#    Copyright (C) 2010 PyPRP2 Project Team
#    See the file AUTHORS for more info about the team.
#    
#    PyPRP2 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    
#    PyPRP2 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with PyPRP2.  If not, see <http://www.gnu.org/licenses/>.


import bpy
from bpy.props import *
from PyHSPlasma import *
from plasma import modifiers
from plasma import geometry
from plasma import physics
from plasma import material
from plasma import lights
from plasma import animations
from plasma import utils
from plasma.utils import PlasmaConfigParser
import os

class VisibleObjectStuff: #do YOU have a better name for it? ;P
    def __init__(self, agename, pagename):
        self.geomgr = geometry.GeometryManager(agename, pagename)
        self.materials = {} #keyed by Blender material
        self.lights = {} #keyed by Blender lights

def export_clean(path,agename): #deletes old files before export
    items = os.listdir(path)
    for item in items:
        if item.startswith(agename):
            os.remove(os.path.join(path,item))

def convert_version(spv):
    if spv == "PVPRIME":
        return pvPrime
    elif spv == "PVPOTS":
        return pvPots
    elif spv == "PVLIVE":
        return pvLive
    elif spv == "PVEOA":
        return pvEoa
    elif spv == "PVHEX":
        return pvHex

def export_scene_as_prp(rm, loc, blscene, agename, path):
    vos = VisibleObjectStuff(agename, blscene.name)
    ExportAllMaterials(rm, loc, blscene, vos)
    ExportSceneNode(rm, loc, blscene,blscene.name,agename, vos)
    vos.geomgr.FinallizeAllDSpans()
    page = plPageInfo()
    page.location = loc
    page.age = agename
    page.page = blscene.name
    rm.AddPage(page)
    fullpagename = "%s_District_%s.prp"%(page.age, page.page)
    print("Writing Page %s"%fullpagename)
    rm.WritePage(os.path.join(path,fullpagename), page)
    GeoMgr = None #clean up

class PlasmaExportAge(bpy.types.Operator):
    '''Export as Plasma Age'''
    bl_idname = "export.plasmaage"
    bl_label = "Export Age"

    def execute(self, context):
        cfg = PlasmaConfigParser()
        exportpath = cfg.get('Paths', 'exportpath')
        if exportpath == None:
            raise Exception("Can't find variable exportpath in config.")
        if len(bpy.data.worlds) > 1:
            raise Exception("Multiple worlds have been detected, please delete all except one of them to continue.")

        plsettings = bpy.data.worlds[0].plasma_age        
        agename = plsettings.name
        if not agename:
            raise Exception("You must give your age a name!")
        print("Cleaning up old files...",end=" ")
        export_clean(exportpath, agename)
        print("Done")
        pversion = convert_version(plsettings.plasmaversion)
        rm = plResManager(pversion)
        ageinfo = plAgeInfo()
        ageinfo.name = agename
        ageinfo.dayLength = plsettings.daylength
        ageinfo.seqPrefix = plsettings.prefix
        ageinfo.maxCapacity = plsettings.maxcapacity
        ageinfo.lingerTime = plsettings.lingertime
        ageinfo.releaseVersion = plsettings.releaseversion
        if plsettings.startdaytime > 0:
            ageinfo.startDayTime = plsettings.startdaytime
        
        for scene in bpy.data.scenes:
            if not scene.plasma_page.isexport:
                continue
            pageid = scene.plasma_page.id
            loc = plLocation()
            loc.page = pageid
            loc.prefix = plsettings.prefix
            export_scene_as_prp(rm, loc, scene, agename, exportpath)
            pageflags = 0
            if not scene.plasma_settings.loadpage:
                pgflags  |= kFlagPreventAutoLoad
            ageinfo.addPage((scene.name,pageid,pageflags))
        print("Writing age file to %s"%os.path.join(exportpath,agename+".age"))
        ageinfo.writeToFile(os.path.join(exportpath,agename+".age"), pversion)
        print("Writing fni file...")
        #just make something default for now
        fnifile = plEncryptedStream(pversion)
        fnifile.open(os.path.join(exportpath,agename+".fni"), fmWrite, plEncryptedStream.kEncAuto)
        fnifile.writeLine("Graphics.Renderer.Setyon 1000000")
        fnifile.writeLine("Graphics.Renderer.Fog.SetDefColor 0 0 0")
        fnifile.writeLine("Graphics.Renderer.SetClearColor 0 0 0")
        fnifile.close()
        print("Writing sum file...")
        sumfile = plEncryptedStream(pversion)
        sumfile.open(os.path.join(exportpath,agename+".sum"), fmWrite, plEncryptedStream.kEncAuto)
        sumfile.writeInt(0)
        sumfile.writeInt(0)
        sumfile.close()
        print("Export Complete")
        return {'FINISHED'}

class PlasmaExportResourcePage(bpy.types.Operator):
    '''Export as Plasma Resource Page'''
    bl_idname = "export.plasmaprp"
    bl_label = "Export PRP"

    filename = StringProperty(name="File Name")
    directory = StringProperty(name="Directory")
    path = StringProperty(name="File Path", description="File path used for exporting the PRP file", maxlen= 1024, default= "")
    use_setting = BoolProperty(name="Example Boolean", description="Example Tooltip", default= True)

    version = EnumProperty(attr="plasma_version",
                              items=(
                                  ("PVPRIME", "Plasma 2.0 (59.11)", "Ages Beyond Myst, To D'ni, Untìl Uru"),
                                  ("PVPOTS", "Plasma 2.0 (59.12)", "Path of the Shell, Complete  Chronicles"),
                                  ("PVLIVE", "Plasma 2.0 (70.9)", "Myst Online: Uru Live, MOULagain, MagiQuest Online"),
                                  ("PVEOA", "Plasma 2.1", "End of Ages, Crowthistle"),
                                  ("PVHEX", "Plasma 3.0", "HexIsle")
                              ),
                              name="Plasma Version",
                              description="Plasma Engine Version",
                              default="PVPOTS")

    def execute(self, context):
        print("Exporting as prp...")
        if len(bpy.data.worlds) > 1:
            raise Exception("Multiple worlds have been detected, please delete all except one of them to continue.")
        
        try:
            plsettings = bpy.data.worlds[0].plasma_age
        except:
            raise Exception("Please go take a look at your world settings.  That's the little globe button.")
        cfg = PlasmaConfigParser()
        
        agename = plsettings.name
        rm = plResManager(convert_version(self.properties.version))
        i = 0
        loc = plLocation()
        loc.page = 0
        loc.prefix = plsettings.prefix
        export_scene_as_prp(rm, loc, bpy.data.scenes[0], agename, self.properties.path)
        print("Export Complete")
        return {'FINISHED'}
    def invoke(self, context, event):
        wm = context.manager
        wm.add_fileselect(self) # will run self.execute()
        return {'RUNNING_MODAL'}

def ExportAvAnimPage():  #this function is so hacky it should be euthanized along with the companion cube
    cfg = PlasmaConfigParser()
    exportpath = cfg.get('Paths', 'exportpath')
    if exportpath == None:
        raise Exception("Can't find variable exportpath in config.")
    if len(bpy.data.worlds) > 1:
        raise Exception("Multiple worlds have been detected, please delete all except one of them to continue.")
    try:
        plsettings = bpy.data.worlds[0].plasma_settings
    except:
        raise Exception("Please go take a look at your world settings.  That's the little globe button.")            
    agename = plsettings.agename
    if not agename:
        raise Exception("You must give your age a name!")

    pversion = convert_version(plsettings.plasmaversion)    
    rm = plResManager(pversion)
    loc = plLocation()
    loc.page = 0 #:P
    loc.prefix = plsettings.prefix

    pagename = bpy.data.scenes[0].name
#fun ;)
    node = plSceneNode("%s_District_%s"%(agename, pagename))
    rm.AddObject(loc,node)
    atcanim = animations.processArmature(bpy.data.scenes[0].objects["PlasmaArmature"],pagename)
    rm.AddObject(loc,atcanim)
    node.addPoolObject(atcanim.key)

    page = plPageInfo()
    page.location = loc
    page.age = agename
    page.page = pagename
    rm.AddPage(page)
    fullpagename = "%s_District_%s.prp"%(page.age, page.page)
    print("Writing Page %s"%fullpagename)
    rm.WritePage(os.path.join(exportpath,fullpagename), page)


class PlasmaExport(bpy.types.Operator):
    bl_idname = "export.plasmaexport"
    bl_label = "Plasma Export"
    type = EnumProperty(items=(
                                  ("age", "Export Age", ""),
                                  ("prp", "Export PRP", ""),
                                  ("aaprp", "Avatar Animation Page (testing use ONLY)", "")
                              ),
                              name="Export Type",
                              description="Export Type")
    def execute(self, context):
        if self.properties.type == "age":
            bpy.ops.export.plasmaage()
        elif self.properties.type == "prp":
            bpy.ops.export.plasmaprp('INVOKE_DEFAULT', path="/")
        elif self.properties.type == "aaprp":
            ExportAvAnimPage()
        ##TODO have an "Export Append" option that splices your pages into an existing age
        return {'FINISHED'}

###### End of Blender operator stuff ######

def ExportAllMaterials(rm, loc, blScn, vos):
    for blObj in blScn.objects:
        for materialslot in blObj.material_slots:
            mat = materialslot.material
            if not mat in vos.materials: #if we haven't already added it
                material.ExportMaterial(rm, loc, mat, vos)

def ExportSceneNode(rm,loc,blScn,pagename,agename, vos):
    name = "%s_District_%s"%(agename, pagename)
    node = plSceneNode(name)
    rm.AddObject(loc,node)
    #hacky adding the dspans here.  When we have more than one dspans it may be better to put it in the geom manager.
##    dspans = geometry.CreateDrawableSpans(agename,node,0,0,pagename) 
#    rm.AddObject(loc,dspans)
#    vos.geomgr.AddDrawableSpans(dspans)
#get those lamps to export first
    for blObj in blScn.objects:
        if blObj.type == "LAMP":
            plScnObj = ExportSceneObject(rm, loc, blObj, vos)
            node.addSceneObject(plScnObj.key)
            
    for blObj in blScn.objects:
        if blObj.type != "LAMP":
            plScnObj = ExportSceneObject(rm, loc, blObj, vos)
            node.addSceneObject(plScnObj.key)
    return node


def ExportSceneObject(rm,loc,blObj, vos):
    print("[Exporting %s]"%blObj.name)
    so = plSceneObject(blObj.name)
    rm.AddObject(loc, so)
    so.sceneNode = rm.getSceneNode(loc).key
    hasCI = False
    try:
        blmods = blObj.plasma_settings.modifiers
    except:
        blmods = None
    #if blmods:
    #    modifiers.Modifiers.Export(rm, loc, blmods,so)
    #    if modifiers.HasModifier(blmods, "spawn"):
    #        hasCI = True #mods force things on here
    if len(blmods) > 0:
        for mod in blmods:
            getattr(bpy.types, 'OBJECT_OT_' + mod.modclass).Export(rm, so, mod)
    if blObj.plasma_settings.isdrawable:
        hasCI = True
    if blObj.type == "LAMP":
        hasCI = True #force CI for lamp
        light = lights.ExportLamp(rm, loc, blObj, vos, so).key
        vos.lights[blObj] = light
        so.addInterface(light)
    elif blObj.type == "EMPTY":
        hasCI = True
    elif blObj.type == "MESH":
        print("    as a mesh")
        try:
            physics = blObj.plasma_settings.physicsenabled
        except:
            physics = False
        print("    with a physical")
        if physics:
            so.sim = ExportSimInterface(rm,loc,blObj,so).key
        #drawable
        try:
            isdrawable = blObj.plasma_settings.isdrawable
        except:
            isdrawable = False
        print("    as a drawable")
        if isdrawable:
            so.draw = ExportDrawInterface(rm,loc,blObj,so,hasCI,vos).key
    if hasCI:
        print("With CI")
        so.coord = ExportCoordInterface(rm,loc,blObj,so).key

    return so

def ExportCoordInterface(rm,loc,blObj,so):
    ci = plCoordinateInterface(blObj.name)
    ci.owner = so.key
    #matrix fun
    l2w = utils.blMatrix44_2_hsMatrix44(blObj.matrix)
    ci.localToWorld = l2w
    ci.localToParent = l2w
    matcopy = blObj.matrix.__copy__()
    matcopy.invert()
    w2l = utils.blMatrix44_2_hsMatrix44(matcopy)
    ci.worldToLocal = w2l
    ci.parentToLocal = w2l
    
    rm.AddObject(loc,ci)
    return ci

def ExportDrawInterface(rm,loc,blObj,so, hasCI,vos):
    di = plDrawInterface(blObj.name)
    di.owner = so.key
    renderlevel = 0
    #deciding what render level/criteria is currently very crude
    if blObj.data.vertex_colors.get("Alpha"): #if we have vertex alpha paint
        renderlevel |= (plRenderLevel.kBlendRendMajorLevel << plRenderLevel.kMajorShift)
    passindxstr = ""
    if blObj.pass_index != 0:
        passindxstr = str(blObj.pass_index)
    spanind = vos.geomgr.FindOrCreateDrawableSpans(rm, loc, renderlevel, 0, passindxstr)
    dspans,diind = vos.geomgr.AddBlenderMeshToDSpans(spanind,blObj, hasCI, vos) #export our mesh
    di.addDrawable(dspans.key,diind)
    rm.AddObject(loc,di)
    return di

def ExportSimInterface(rm,loc,blObj,so):
    si = plSimulationInterface(blObj.name)
    si.owner = so.key
    si.physical = physics.Physical.Export(rm,loc,blObj,so).key
    rm.AddObject(loc,si)
    return si

