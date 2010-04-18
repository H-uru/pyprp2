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
import os
import os.path
import sys
import plasma

def add_mod_menu(mod):
    lambda self, context: self.layout.operator(mod.bl_idname, text=mod.bl_label)

class PlasmaModifierMenu(bpy.types.Menu):
    bl_idname = 'PlasmaModifierMenu'
    bl_label = 'Add Modifier'

    submenus = []

    __menuid = 'PlasmaModifierCat{0}'
    __menucls = "class {0}(bpy.types.Menu):\n    bl_idname = '{0}'\n    bl_label = '{1}'\n    def draw(self, context):\n        self.layout.operator_context = 'EXEC_AREA'\nbpy.types.register({0})"

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

class PlasmaModifierSettings(bpy.types.IDPropertyGroup):
    pass
    
PlasmaModifierSettings.StringProperty(attr = 'modclass', name = 'Type', default = '')
PlasmaModifierSettings.StringProperty(attr = 'modname', name = 'Name', default = '')


class PlasmaModifierPanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "constraint"
    bl_label = "Plasma Modifiers"

    def draw(self, context):
        layout = self.layout

        ob = context.object
        layout.label(text = 'Attached Modifiers:')
        row = layout.row()
        row.template_list(ob.plasma_settings, 'modifiers', ob.plasma_settings, 'activemodifier', rows = 2)

        col = row.column(align = True)
        col.menu('PlasmaModifierMenu', icon = 'ZOOMIN', text = '')

def register():
    bpy.types.register(PlasmaModifierSettings)
    bpy.types.register(PlasmaModifierMenu)
    bpy.types.register(PlasmaModifierPanel)

    bpy.types.Object.PointerProperty(attr = 'plasma_settings',
                                    type = bpy.types.PlasmaSettings,
                                    name = 'Plasma Settings',
                                    description = 'Plasma Engine Object Settings')
    bpy.types.PlasmaSettings.CollectionProperty(attr = 'modifiers', type = PlasmaModifierSettings)
    bpy.types.PlasmaSettings.IntProperty(attr = 'activemodifier', default = 0)

    modpath = os.path.join(os.path.dirname(plasma.__file__), "mods/")
    mods = [fname[:-3] for fname in os.listdir(modpath) if fname.endswith('.py')]
    if not modpath in sys.path:
        sys.path.append(modpath)
    modifiers = [__import__(mname) for mname in mods]
    [[PlasmaModifierMenu.AddModifier(bmod) for bmod in mod.register()] for mod in modifiers]
