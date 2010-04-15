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
import copy

def HasModifier(blmods,modtype):
    for blmod in blmods:
        if blmod.type == modtype:
            return True
    return False

def GetModifierClass(typestr):
    if typestr == "spawn":
        return Spawn
    elif typestr == "waveset":
        return Waveset

#so many static methods...
class ModifierInfo:
    def CreateProps(mod):
        pass
    CreateProps = staticmethod(CreateProps)
    def Draw(self, context, mod):
        pass
    Draw = staticmethod(Draw)
    def Export(mod,plmod):
        pass
    Export = staticmethod(Export)
    def Copy(src,dest):  #there has to be a better way to copy props to an existing class
        pass
    Export = staticmethod(Copy)

class Waveset(ModifierInfo):
    def Draw(self, context, mod):
        layout = self.layout
        layout.label(text="No Waveset support yet")

class Spawn(ModifierInfo):
    pass


def CopyModifierFunc(srcmod,modifiers):
    #if it's already there create a new name
    newmod = modifiers.add()
    if modifiers.get(srcmod.name) == None:
        newmod.name = srcmod.name
    else:
        trynum = 1
        while modifiers.get(srcmod.name+str(trynum)):
            trynum+=1
        newmod.name = srcmod.name+str(trynum)
    newmod.type = srcmod.type
    GetModifierClass(srcmod.type).Copy(srcmod, newmod)
            
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
    GetModifierClass(typestr).CreateProps(newmod)

class CopyModifierToSelected(bpy.types.Operator):
    bl_idname = "object.plcopymodifier"
    bl_label = "Copy Modifier to Selected Object"

    def execute(self, context):
        srcmod = context.object.plasma_settings.modifiers[context.object.plasma_settings.activemodifier]
        for ob in [ob for ob in context.scene.objects if ob.type == "MESH" and ob.selected and ob != context.object]:
            CopyModifierFunc(srcmod, ob.plasma_settings.modifiers)
        return {'FINISHED'}

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
        context.object.plasma_settings.activemodifier-=1
        return {'FINISHED'}

class PlasmaModifierSettings(bpy.types.IDPropertyGroup):
    pass
PlasmaModifierSettings.StringProperty(attr="type", name="Type", default="")

class Modifiers(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "modifier"
    bl_label = "Plasma Modifiers"
    def InitProperties():
        bpy.types.Object.PointerProperty(attr="plasma_settings", type=bpy.types.PlasmaSettings, name="Plasma Settings", description="Plasma Engine Object Settings")
        bpy.types.PlasmaSettings.CollectionProperty(attr="modifiers", type=PlasmaModifierSettings)
        bpy.types.PlasmaSettings.IntProperty(attr="activemodifier",default=0)
    InitProperties = staticmethod(InitProperties)
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
            layout.operator("object.plcopymodifier", text="Copy to Selected")
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
    bpy.types.register(CopyModifierToSelected)
    bpy.types.register(AddModifier)
    bpy.types.register(RemoveModifier)
    Modifiers.InitProperties()
    bpy.types.register(Modifiers)

def unregister():
    bpy.types.unregister(PlasmaModifierSettings)
    bpy.types.unregister(CopyModifierToSelected)
    bpy.types.unregister(AddModifier)
    bpy.types.unregister(RemoveModifier)
    bpy.types.unregister(Modifiers)