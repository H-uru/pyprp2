import bpy
from PyHSPlasma import *
from bpy.props import *
import modifiers
version = pvPots

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

    type = bpy.props.EnumProperty(items=(('OPT_A', "First Option", "Description one"), ('OPT_B', "Second Option", "Description two.")),
                        name="Example Enum",
                        description="Choose between two items",
                        default='OPT_A')

    def execute(self, context):
        print("Exporting as prp...")
        rm = plResManager(version)
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



