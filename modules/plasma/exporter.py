import bpy
from PyHSPlasma import *
from bpy.props import *
import modifiers,geometry,physics


GeoMgr = geometry.GeometryManager()
    

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
    ExportSceneNode(rm, loc, blscene,blscene.name,agename)
    #quicky mat
    mat = hsGMaterial("mat")
    rm.AddObject(loc,mat)
    layer = plLayer("layer")
    rm.AddObject(loc,layer)
    mat.addLayer(layer.key)
    #end of quicky mat
    GeoMgr.FinallizeDSpans(0,mat)
    page = plPageInfo()
    page.location = loc
    page.age = agename
    page.page = bpy.data.scenes[0].name
    rm.AddPage(page)
    fullpagename = "%s_District_%s.prp"%(page.age, page.page)
    print("Writing Page %s"%fullpagename)
    rm.WritePage(path, page)

        


class PlasmaExportAge(bpy.types.Operator):
    '''Export as Plasma Age'''
    bl_idname = "export.plasmaage"
    bl_label = "Export Age"

    filename = StringProperty(name="File Name")
    directory = StringProperty(name="Directory")
    path = StringProperty(name="Directory", description="Directory used for exporting the Age", maxlen= 1024, default= "")
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
        raise Exception("not implemented yet")
        return {'FINISHED'}
    def invoke(self, context, event):
        wm = context.manager
        wm.add_fileselect(self) # will run self.execute()
        return {'RUNNING_MODAL'}

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
        agename = "test_pyprp2"
        rm = plResManager(convert_version(self.properties.version))
        i = 0
        loc = plLocation()
        loc.page = 0
        loc.prefix = 299
        export_scene_as_prp(rm, loc, bpy.data.scenes[0], agename, self.properties.path)
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
            bpy.ops.export.plasmaage('INVOKE_DEFAULT', path="/")
        elif self.properties.type == "prp":
            bpy.ops.export.plasmaprp('INVOKE_DEFAULT', path="/")
        return {'FINISHED'}

###### End of Blender operator stuff ######

def ExportSceneNode(rm,loc,blScn,pagename,agename):
    name = "%s_District_%s"%(agename, pagename)
    node = plSceneNode(name)
    rm.AddObject(loc,node)
    #hacky adding the dspans here.  When we have more than one dspans it may be better to put it in the geom manager.
    dspans = geometry.CreateDrawableSpans(agename,node,0,0,pagename) 
    rm.AddObject(loc,dspans)
    GeoMgr.AddDrawableSpans(dspans)

    for blObj in blScn.objects:
        plScnObj = ExportSceneObject(rm, loc, blObj)
        node.addSceneObject(plScnObj.key)
    return node


def ExportSceneObject(rm,loc,blObj):
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
    if hasCI:
        print("With CI")
        so.coord = ExportCoordInterface(rm,loc,blObj,so).key
    #get down to object types
    if blObj.type == "MESH":
        print("    as a mesh")
        try:
            physics = blObj.plasma_settings.physicsenabled
        except:
            physics = False
        print("    with a physical")
        if physics:
            so.sim = ExportSimInterface(rm,loc,blObj,so).key
        so.draw = ExportDrawInterface(rm,loc,blObj,so,hasCI).key
    rm.AddObject(loc, so)
    return so

def ExportCoordInterface(rm,loc,blObj,so):
    ci = plCoordinateInterface(blObj.name)
    ci.owner = so.key
    #matrix fun
    l2w = geometry.blMatrix44_2_hsMatrix44(blObj.matrix)
    ci.localToWorld = l2w
    ci.localToParent = l2w
    matcopy = blObj.matrix.__copy__()
    matcopy.invert()
    w2l = geometry.blMatrix44_2_hsMatrix44(matcopy)
    ci.worldToLocal = w2l
    ci.parentToLocal = w2l
    
    rm.AddObject(loc,ci)
    return ci

def ExportDrawInterface(rm,loc,blObj,so, hasCI):
    di = plDrawInterface(blObj.name)
    di.owner = so.key
    dspans,diind = GeoMgr.AddBlenderMeshToDSpans(0,blObj, hasCI) #export our mesh
    di.addDrawable(dspans.key,diind)
    rm.AddObject(loc,di)
    return di

def ExportSimInterface(rm,loc,blObj,so):
    si = plSimulationInterface(blObj.name)
    si.owner = so.key
    si.physical = physics.Physical.Export(rm,loc,blObj,so).key
    rm.AddObject(loc,si)
    return si

