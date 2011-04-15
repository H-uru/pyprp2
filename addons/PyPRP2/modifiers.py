#    This file is part of PyPRP2.
#    
#    Copyright (C) 2010 PyPRP2 Project Team
#    See the file AUTHORS for more info about the team.
#    
#    PyPRP2 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    
#    PyPRP2 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with PyPRP2.  If not, see <http://www.gnu.org/licenses/>.

import bpy
from bpy.props import *
import os
import os.path
import sys


def add_mod_menu(mod):
    return lambda self, context: self.layout.operator(mod.bl_idname, text=mod.bl_label)

class PlasmaModifierMenu(bpy.types.Menu):
    bl_idname = 'PlasmaModifierMenu'
    bl_label = 'Add Modifier'
    bl_description = 'Add a new modifier'

    submenus = []

    __menuid = 'PlasmaModifierCat{0}'
    __menucls = "class {0}(bpy.types.Menu):\n    bl_idname = '{0}'\n    bl_label = '{1}'\n    def draw(self, context):\n        self.layout.operator_context = 'EXEC_AREA'\nbpy.utils.register_class({0})"

    @staticmethod
    def AddCategory(name):
        mnuid = PlasmaModifierMenu.__menuid.format(name)
        mnucls = PlasmaModifierMenu.__menucls.format(mnuid, name)
        exec(mnucls) #EVIL Hack

        PlasmaModifierMenu.submenus.append(mnuid)

    @staticmethod
    def AddModifier(mod):
        mnuid = PlasmaModifierMenu.__menuid.format(mod.category)
        if not mnuid in PlasmaModifierMenu.submenus:
            PlasmaModifierMenu.AddCategory(mod.category)

        getattr(bpy.types, mnuid).append(add_mod_menu(mod))

    def draw(self, context):
        layout = self.layout
        
        for mnu in PlasmaModifierMenu.submenus:
            layout.menu(mnu)

class PlasmaModifierSettings(bpy.types.PropertyGroup):
    modclass = StringProperty(attr = 'modclass', name = 'Type', default = '')

class PlasmaModifierRemove(bpy.types.Operator):
    bl_idname = 'object.plremovemodifier'
    bl_label = 'Remove Modifier'
    bl_description = 'Remove the active modifier'

    @classmethod
    def poll(self, context):
        return context.active_object != None
        
    def execute(self, context):
        ob = context.object
        pl = ob.plasma_settings

        pl.modifiers.remove(pl.activemodifier)
        pl.activemodifier -= 1
        return {'FINISHED'}

class PlasmaModifierPanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'constraint'
    bl_label = 'Plasma Modifiers'

    def draw(self, context):
        layout = self.layout

        ob = context.object
        layout.label(text = 'Attached Modifiers:')
        row = layout.row()
        col = row.column()
        col.template_list(ob.plasma_settings, 'modifiers', ob.plasma_settings, 'activemodifier', rows = 2)

        col = row.column(align = True)
        col.menu('PlasmaModifierMenu', icon = 'ZOOMIN', text = '')
        col.operator('object.plremovemodifier', icon = 'ZOOMOUT', text = '')

        pl = ob.plasma_settings
        if len(pl.modifiers) > 0:
            mod = pl.modifiers[pl.activemodifier]
            box = layout.box()
            box.prop(mod, 'name', text = 'Name')
            
            row = box.row()
            row.active = False
            row.enabled = False
            row.prop(mod, 'modclass', text = 'Type')
            
            

def register():
    bpy.utils.register_class(PlasmaModifierMenu)
    bpy.utils.register_class(PlasmaModifierSettings)
    bpy.utils.register_class(PlasmaModifierRemove)
    bpy.utils.register_class(PlasmaModifierPanel)
    modpath = os.path.join(os.path.split(__file__)[0],"mods/")
    mods = [fname[:-3] for fname in os.listdir(modpath) if fname.endswith('.py')]
    if not modpath in sys.path:
        sys.path.append(modpath)
    modifiers = [__import__(mname) for mname in mods]
    [[PlasmaModifierMenu.AddModifier(bmod) for bmod in mod.register()] for mod in modifiers]

def unregister():
    modpath = os.path.join(os.path.split(__file__)[0],"mods/")
    mods = [fname[:-3] for fname in os.listdir(modpath) if fname.endswith('.py')]
    if not modpath in sys.path:
        sys.path.append(modpath)
    modifiers = [__import__(mname) for mname in mods]
    [mod.unregister() for mod in modifiers]
    bpy.utils.unregister_class(PlasmaModifierPanel)
    bpy.utils.unregister_class(PlasmaModifierRemove)
    bpy.utils.unregister_class(PlasmaModifierSettings)
    bpy.utils.unregister_class(PlasmaModifierMenu)