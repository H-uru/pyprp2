from plasma_namespace import *
from bpy.props import *

def AddModifier(modifiers,typestr):
    #if it's already there create a new name
    newmod = modifiers.add()
    if modifiers.get(typestr) == None:
        newmod.name = typestr
    else:
        trynum = 1
        while modifiers.get(typestr+str(trynum)):
            trynum+=1
        newmod.name = typestr+str(trynum)
        
    newmod.StringProperty(attr="type", default=typestr)
    print("Adding %s"%newmod.name)
    if typestr == "plSpawnModifier":
        newmod.FloatProperty(attr="test")

class PlCreateSpawnModifier(bpy.types.Operator):
    bl_idname = "object.plcreatespawnmodifier"
    bl_label = "Create a Spawn Mod"
    def poll(self, context):
        return context.active_object != None
    def execute(self, context):
        AddModifier(context.object.plasma_settings.modifiers,"plSpawnModifier")
        return {'FINISHED'}

class PlCreateWavesetModifier(bpy.types.Operator):
    bl_idname = "object.plcreatewavesetmodifier"
    bl_label = "Create a Waveset Mod"
    def poll(self, context):
        return context.active_object != None
    def execute(self, context):
        AddModifier(context.object.plasma_settings.modifiers,"plWavesetModifier")
        return {'FINISHED'}

class PlAddModifierMenu(bpy.types.Menu):
    bl_idname = "PlAddModifierMenu"
    bl_label = "Add Plasma Modifier"

    def draw(self, context):
        layout = self.layout
        
        layout.operator_context = 'EXEC_AREA'
        layout.operator("object.plcreatespawnmodifier", text="Spawn Point")
        layout.operator("object.plcreatewavesetmodifier", text="Waveset")
class plModifierSettings(bpy.types.IDPropertyGroup):
    pass


class PlasmaModTypes(bpy.types.Menu):
    bl_idname = "PlasmaModTypes"
    bl_label = "New Plasma Modifier"

    def draw(self, context):
        layout = self.layout
        
        layout.operator("export.plasmaexportprp", text="Export Prp")
        layout.operator("wm.exit_blender", text="Quit", icon='QUIT')


class plasma_modifiers(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "modifier"
    bl_label = "Plasma Modifiers"
    
    bpy.types.Object.PointerProperty(attr="plasma_settings", type=PlasmaSettings, name="Plasma Settings", description="Plasma Engine Object Settings")
    PlasmaSettings.CollectionProperty(attr="modifiers", type=plModifierSettings)
    def draw(self, context):
        layout = self.layout

        ob = context.object
        pl = ob.plasma_settings
        layout.menu("PlAddModifierMenu")
        #layout.template_ID(ob, "parent")
        #layout.template_list(pl, "plModifiers", pl, "custom", rows=2)
        for modkey in pl.modifiers.keys():
            layout.label(text=modkey)
            #box = layout.template_modifier(md)

mod_creators = [PlCreateSpawnModifier, PlCreateWavesetModifier]

def register():
    for mc in mod_creators:
        bpy.types.register(mc)
    bpy.types.register(PlAddModifierMenu)
    bpy.types.register(plasma_modifiers)


def unregister():
    for mc in mod_creators:
        bpy.types.unregister(mc)
    bpy.types.unregister(PlAddModifierMenu)
    bpy.types.unregister(plasma_modifiers)
