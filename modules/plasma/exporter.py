import bpy
from PyHSPlasma import *
from bpy.props import *
import modifiers

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

class PlasmaExportPrp(bpy.types.Operator): #having this separate operator sucks, if there's a simpler way to do this please change it
    bl_idname = "export.plasmaexportprp"
    bl_label = "PlasmaExportPrp"
    def execute(self, context):
        bpy.ops.export.prp('INVOKE_DEFAULT', path="/")
        return {'FINISHED'}
    
class PlasmaExportResourcePage(bpy.types.Operator):
    '''Export as Plasma Resource Page'''
    bl_idname = "export.prp"
    bl_label = "Export PRP"

    filename = StringProperty(name="File Name")
    directory = StringProperty(name="Directory")
    path = StringProperty(name="File Path", description="File path used for exporting the PLY file", maxlen= 1024, default= "")
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
                              default="PVPOTS") #bpy.types.Window.

    def execute(self, context):
        print("Exporting as prp...")
        rm = plResManager(convert_version(self.properties.version))
        i = 0
        loc = plLocation()
        loc.page = 0
        loc.prefix = i
    
        ExportSceneNode(rm, loc, bpy.data.scenes[0])
        page = plPageInfo()
        page.location = loc
        page.age = "agename"
        page.page = bpy.data.scenes[0].name
        rm.AddPage(page)
        #rm.WritePage(os.path.join(path,pageName)+'.prp', page)
        rm.WritePage(self.properties.path, page)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.manager
        wm.add_fileselect(self) # will run self.execute()
        return {'RUNNING_MODAL'}

def ExportSceneNode(rm,loc,blScn):
    node = plSceneNode(blScn.name)
    rm.AddObject(loc,node)
    for blObj in blScn.objects:
        plScnObj = ExportSceneObject(rm, loc, blObj)
        node.addSceneObject(plScnObj.key)
    return node
    

def ExportSceneObject(rm,loc,blObj):
    print("[Exporting %s]"%blObj.name)
    so = plSceneObject(blObj.name)

    so.sceneNode = rm.getSceneNode(loc).key
    if blObj.type == "MESH":
        print("    as a mesh")
        so.draw = ExportDrawInterface(rm,loc,blObj,so).key
    modifiers.Modifiers.Export(rm, loc, blObj.plasma_settings.modifiers,so)
    rm.AddObject(loc, so)
    return so

def ExportDrawInterface(rm,loc,blObj,so):
    di = plDrawInterface(blObj.name)
    di.owner = so.key
    rm.AddObject(loc,di)
    return di



