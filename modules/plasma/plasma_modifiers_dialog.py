from plasma_namespace import *
from bpy.props import *


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
    newmod.StringProperty(attr="type", name="Type", default=typestr)
    newmod.type = typestr
    print("Adding a %s"%newmod.type)
    if typestr == "spawn":
        newmod.FloatProperty(attr="test")

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
        return {'FINISHED'}

    
class RemoveModifier(bpy.types.Operator):
    bl_idname = "object.plremovemodifier"
    bl_label = "Remove the active modifier"
    def poll(self, context):
        return context.active_object != None
    def execute(self, context):
        context.object.plasma_settings.modifiers.remove(context.object.plasma_settings.activemodifier)
        return {'FINISHED'}

class ModifierSettings(bpy.types.IDPropertyGroup):
    pass

class plasma_modifiers(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "modifier"
    bl_label = "Plasma Modifiers"
    
    bpy.types.Object.PointerProperty(attr="plasma_settings", type=PlasmaSettings, name="Plasma Settings", description="Plasma Engine Object Settings")
    PlasmaSettings.CollectionProperty(attr="modifiers", type=ModifierSettings)
    PlasmaSettings.IntProperty(attr="activemodifier",default=0)
    def draw(self, context):
        layout = self.layout

        ob = context.object
        pl = ob.plasma_settings
        #layout.menu("PlAddModifierMenu")
        #layout.template_ID(ob, "parent")
        
        
        layout.label(text="Attached Plasma Modifiers:")
        row = layout.row()
        row.template_list(pl, "modifiers", pl, "activemodifier", rows=2)
        col = row.column(align=True)
        col.operator_menu_enum("object.pladdmodifier","type", icon='ZOOMIN', text="")
        col.operator("object.plremovemodifier", icon='ZOOMOUT', text="")
        
        if len(pl.modifiers) > 0: #if we have some mods
            mod = pl.modifiers[pl.activemodifier]
            layout.prop(mod,"name")
            if mod.type == "spawn":
                pass #no other settings than name to draw
            elif mod.type == "waveset":
                self.drawWaveset(context, mod)
    def drawWaveset(self, context, mod):
        layout = self.layout
        layout.label(text="I am a Wave")


def register():
    bpy.types.register(AddModifier)
    bpy.types.register(RemoveModifier)
    bpy.types.register(plasma_modifiers)


def unregister():
    bpy.types.register(AddModifier)
    bpy.types.unregister(RemoveModifier)
    bpy.types.unregister(plasma_modifiers)
