import bpy
from bpy.props import *

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
    bpy.types.Object.FloatProperty(attr="testprop",name="Mass")
    bpy.types.Object.PointerProperty(attr="custom", name="custom", type=bpy.types.IDPropertyGroup)
    bpy.types.Object.CollectionProperty(attr="plModifiers", type=bpy.types.IDPropertyGroup)
                                 
    #bpy.types.Object.EnumProperty(attr="plModifiers", items=(("None", "Box",""),("test", "Sphere","")), name="plModifiers")
    def draw(self, context):
        layout = self.layout

        ob = context.object

        #layout.operator_menu_enum("object.modifier_add", "testprop")
        #layout.template_ID(ob, "parent")
        layout.menu("INFO_MT_file")
        layout.template_list(ob, "plModifiers", ob, "custom", rows=2)
        
        for md in ob.modifiers:
            box = layout.template_modifier(md)
            #if box:
                # match enum type to our functions, avoids a lookup table.
             #   getattr(self, md.type)(box, ob, md, wide_ui)

def register():
    bpy.types.register(plasma_modifiers)

def unregister():
    bpy.types.unregister(plasma_modifiers)
