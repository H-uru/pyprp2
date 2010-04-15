#    Copyright (C) 2010  Guild of Writers PyPRP2 Project Team
#    See the file AUTHORS for more info about the team
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#    Please see the file LICENSE for the full license.


import bpy
from PyHSPlasma import *
from bpy.props import *
from plasma import modifiers
from plasma import geometry
from plasma import physics
from plasma import material
from plasma import lights
from plasma import utils
import os

config_name = "pyprp2.conf"

class VisibleObjectStuff: #do YOU have a better name for it? ;P
    def __init__(self):
        self.geomgr = geometry.GeometryManager()
        self.materials = {} #keyed by Blender material


def readConfig(filepath): #tiny little parser
    file = open(filepath)
    lines = file.readlines()
    file.close()
    info = {}
    for line in lines:
        if not line.startswith("#"):
            line = line.strip("\n")
            key,value = line.split("=")
            info[key] = value
    return info

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

def export_scene_as_prp(rm, loc, blscene, agename, path, confdata):
    vos = VisibleObjectStuff()
    ExportAllMaterials(rm, loc, blscene, vos, confdata)
    ExportSceneNode(rm, loc, blscene,blscene.name,agename, vos)
    vos.geomgr.FinallizeDSpans(0)
    page = plPageInfo()
    page.location = loc
    page.age = agename
    page.page = bpy.data.scenes[0].name
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
        dotblenderpath = bpy.utils.home_paths()[1]
        confdata = readConfig(os.path.join(dotblenderpath,config_name))
        exportpath = confdata.get("exportpath")
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
        ageinfo = plAgeInfo()
        ageinfo.name = agename
        ageinfo.dayLength = plsettings.daylength
        ageinfo.seqPrefix = plsettings.ageprefix
        ageinfo.maxCapacity = plsettings.maxcapacity
        ageinfo.lingerTime = plsettings.lingertime
        ageinfo.releaseVersion = plsettings.releaseversion
        if plsettings.startdaytime > 0:
            ageinfo.startDayTime = plsettings.startdaytime
        
        for i, scene in enumerate(bpy.data.scenes):
            loc = plLocation()
            loc.page = i
            loc.prefix = plsettings.ageprefix
            export_scene_as_prp(rm, loc, scene, agename, exportpath, confdata)
            ageinfo.addPage((scene.name,i,0))
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

    version = bpy.props.EnumProperty(attr="plasma_version",
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
            plsettings = bpy.data.worlds[0].plasma_settings
        except:
            raise Exception("Please go take a look at your world settings.  That's the little globe button.")
        dotblenderpath = bpy.utils.home_paths()[1]
        confdata = readConfig(os.path.join(dotblenderpath,config_name))
        
        agename = plsettings.agename
        rm = plResManager(convert_version(self.properties.version))
        i = 0
        loc = plLocation()
        loc.page = 0
        loc.prefix = plsettings.ageprefix
        export_scene_as_prp(rm, loc, bpy.data.scenes[0], agename, self.properties.path,confdata)
        print("Export Complete")
        return {'FINISHED'}
    def invoke(self, context, event):
        wm = context.manager
        wm.add_fileselect(self) # will run self.execute()
        return {'RUNNING_MODAL'}

class PlasmaExport(bpy.types.Operator):
    bl_idname = "export.plasmaexport"
    bl_label = "Plasma Export"
    type = EnumProperty(items=(
                                  ("age", "Export Age", ""),
                                  ("prp", "Export PRP", "")
                              ),
                              name="Export Type",
                              description="Export Type")
    def execute(self, context):
        if self.properties.type == "age":
            bpy.ops.export.plasmaage()
        elif self.properties.type == "prp":
            bpy.ops.export.plasmaprp('INVOKE_DEFAULT', path="/")
        return {'FINISHED'}

###### End of Blender operator stuff ######

def ExportAllMaterials(rm, loc, blScn, vos, confdata):
    for blObj in blScn.objects:
        for materialslot in blObj.material_slots:
            mat = materialslot.material
            if not mat in vos.materials: #if we haven't already added it
                material.ExportMaterial(rm, loc, mat, vos, confdata)

def ExportSceneNode(rm,loc,blScn,pagename,agename, vos):
    name = "%s_District_%s"%(agename, pagename)
    node = plSceneNode(name)
    rm.AddObject(loc,node)
    #hacky adding the dspans here.  When we have more than one dspans it may be better to put it in the geom manager.
    dspans = geometry.CreateDrawableSpans(agename,node,0,0,pagename) 
    rm.AddObject(loc,dspans)
    vos.geomgr.AddDrawableSpans(dspans)
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
    so.sceneNode = rm.getSceneNode(loc).key
    hasCI = False
    try:
        blmods = blObj.plasma_settings.modifiers
    except:
        blmods = None
    if blmods:
        modifiers.Modifiers.Export(rm, loc, blmods,so)
        if modifiers.HasModifier(blmods, "spawn"):
            hasCI = True #mods force things on here
    if blObj.type == "LAMP":
        hasCI = True #force CI for lamp
        so.addInterface(lights.ExportLamp(rm, loc, blObj, vos, so).key)
    if hasCI:
        print("With CI")
        so.coord = ExportCoordInterface(rm,loc,blObj,so).key
    elif blObj.type == "MESH":
        print("    as a mesh")
        try:
            physics = blObj.plasma_settings.physicsenabled
        except:
            physics = False
        print("    with a physical")
        if physics:
            so.sim = ExportSimInterface(rm,loc,blObj,so).key
        so.draw = ExportDrawInterface(rm,loc,blObj,so,hasCI,vos).key
    rm.AddObject(loc, so)
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
    dspans,diind = vos.geomgr.AddBlenderMeshToDSpans(0,blObj, hasCI, vos.materials) #export our mesh
    di.addDrawable(dspans.key,diind)
    rm.AddObject(loc,di)
    return di

def ExportSimInterface(rm,loc,blObj,so):
    si = plSimulationInterface(blObj.name)
    si.owner = so.key
    si.physical = physics.Physical.Export(rm,loc,blObj,so).key
    rm.AddObject(loc,si)
    return si

