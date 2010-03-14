import bpy
from PyHSPlasma import *
from bpy.props import *
version = pvPots



def ExportAsPrp():
    bpy.ops.export.prp('INVOKE_DEFAULT', path="/tmp/test.ply")
    
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
    rm.WritePage("test.prp", page)


def ExportSceneNode(rm,loc,blScn):
    node = plSceneNode(blScn.name)
    rm.AddObject(loc,node)
    for blObj in blScn.objects:
        plScnObj = ExportSceneObject(rm, loc, blObj)
        node.addSceneObject(plScnObj.key)
    return node
    

def ExportSceneObject(rm,loc,blObj):
    so = plSceneObject(blObj.name)
    so.sceneNode = rm.getSceneNode(loc).key
    if blObj.type == "MESH":
        ExportDrawInterface(rm,loc,blObj,so)
    rm.AddObject(loc, so)
    return so

def ExportDrawInterface(rm,loc,blObj,so):
    di = plDrawInterface(blObj.name)
    di.owner = so.key
    rm.AddObject(loc,di)
    return di


class PlasmaExportResourcePage(bpy.types.Operator):
    '''Export as Plasma Resource Page'''
    bl_idname = "export.prp"
    bl_label = "Export PRP"


    # TODO, add better example props
    path = StringProperty(name="File Path", description="File path used for exporting the PLY file", maxlen= 1024, default= "")
    use_setting = BoolProperty(name="Example Boolean", description="Example Tooltip", default= True)

    type = bpy.props.EnumProperty(items=(('OPT_A', "First Option", "Description one"), ('OPT_B', "Second Option", "Description two.")),
                        name="Example Enum",
                        description="Choose between two items",
                        default='OPT_A')

    def poll(self, context):
        return context.active_object != None

    def execute(self, context):
        ExportAsPrp()
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.manager

        if True:
            # File selector
            wm.add_fileselect(self) # will run self.execute()
            return {'RUNNING_MODAL'}
        elif True:
            # search the enum
            wm.invoke_search_popup(self)
            return {'RUNNING_MODAL'}
        elif False:
            # Redo popup
            return wm.invoke_props_popup(self, event) #
        elif False:
            return self.execute(context)
