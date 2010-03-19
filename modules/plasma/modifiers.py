import bpy
from PyHSPlasma import *
from bpy.props import *

#so many static methods...
class Waveset:
    def CreateProps(mod):
        pass
    CreateProps = staticmethod(CreateProps)
    def Draw(self, context, mod):
        layout = self.layout
        layout.label(text="No Waveset support yet")
    Draw = staticmethod(Draw)
    def Export(mod,plmod):
        pass
    Export = staticmethod(Export)

def AddModifierFunc(modifiers,typestr):
    #if it's already there create a new name
    newmod = modifiers.add()
    if modifiers.get(typestr) == None:
        newmod.name = typestr
    else:
        trynum = 1
        while modifiers.get(typestr+str(trynum)):
            trynum+=1
        newmod.name = typestr+str(trynum)
    newmod.type = typestr
    print("Adding a %s"%newmod.type)
    if typestr == "waveset":
        Waveset.CreateProps(newmod)

class AddModifier(bpy.types.Operator):
    bl_idname = "object.pladdmodifier"
    bl_label = "Add a modifier"
    type = EnumProperty(items=(
                                  ("spawn", "Spawn", ""),
                                  ("waveset", "Waveset", "")
                              ),
                              name="Modifier Type",
                              description="Modifier Type")
    def execute(self, context):
        AddModifierFunc(context.object.plasma_settings.modifiers,self.properties.type)
        context.object.plasma_settings.activemodifier = (len(context.object.plasma_settings.modifiers)-1)
        return {'FINISHED'}

    
class RemoveModifier(bpy.types.Operator):
    bl_idname = "object.plremovemodifier"
    bl_label = "Remove the active modifier"
    def poll(self, context):
        return context.active_object != None
    def execute(self, context):
        context.object.plasma_settings.modifiers.remove(context.object.plasma_settings.activemodifier)
        return {'FINISHED'}

class PlasmaModifierSettings(bpy.types.IDPropertyGroup):
    pass
PlasmaModifierSettings.StringProperty(attr="type", name="Type", default="")

class Modifiers(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "modifier"
    bl_label = "Plasma Modifiers"
    def __init__(self, thing1):
        bpy.types.Panel.__init__(self)
        bpy.types.Object.PointerProperty(attr="plasma_settings", type=bpy.types.PlasmaSettings, name="Plasma Settings", description="Plasma Engine Object Settings")
        bpy.types.PlasmaSettings.CollectionProperty(attr="modifiers", type=PlasmaModifierSettings)
        bpy.types.PlasmaSettings.IntProperty(attr="activemodifier",default=0)
    def draw(self, context):
        layout = self.layout

        ob = context.object
        pl = ob.plasma_settings
        #layout.template_ID(ob, "parent")
        
        layout.label(text="List of Attached Mods:")
        row = layout.row()
        row.template_list(pl, "modifiers", pl, "activemodifier", rows=2)
        col = row.column(align=True)
        col.operator_menu_enum("object.pladdmodifier","type", icon='ZOOMIN', text="")
        col.operator("object.plremovemodifier", icon='ZOOMOUT', text="")
        
        if len(pl.modifiers) > 0: #if we have some mods
            mod = pl.modifiers[pl.activemodifier]
            layout.prop(mod,"name")
            layout.label(text="type: %s"%mod.type)
            if mod.type == "spawn":
                pass #no other settings than name to draw
            elif mod.type == "waveset":
                Waveset.Draw(self, context, mod)
    def Export(rm, loc, plblmods, so):
        for mod in plblmods:
            if mod.type == "spawn":
                plmod = plSpawnModifier(mod.name)
                rm.AddObject(loc,plmod)
                so.addModifier(plmod.key)
            else:
                print("type %s not supported, skipping"%mod.type)
    Export = staticmethod(Export)


def register():
    bpy.types.register(PlasmaModifierSettings)
    bpy.types.register(AddModifier)
    bpy.types.register(RemoveModifier)
    bpy.types.register(Modifiers)


def unregister():
    bpy.types.unregister(PlasmaModifierSettings)
    bpy.types.unregister(AddModifier)
    bpy.types.unregister(RemoveModifier)
    bpy.types.unregister(Modifiers)
