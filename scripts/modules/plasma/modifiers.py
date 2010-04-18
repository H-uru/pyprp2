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

class ModBase(bpy.types.operator):
    @staticmethod
    def InitProperties():
        pass

    @staticmethod
    def DelProperties():
        pass

    @staticmethod
    def Export():
        pass

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
        mnuid = __menuid.format(name)
        mnucls = __menucls.format(mnuid, name)
        exec(mnucls) #EVIL Hack

        submenus.append(mnuid)

    @staticmethod
    def AddModifier(mod):
        mnuid = __menuid.format(mod.category)
        if not mnuid in submenus:
            PlasmaModifierMenu.AddCategory(mod.category)

        eval('bpy.types.'+mnuid+'.append(add_mod_menu(mod))')

    def draw(self, context):
        layout = self.layout
        
        for mnu in submenus:
            layout.menu(mnu)
