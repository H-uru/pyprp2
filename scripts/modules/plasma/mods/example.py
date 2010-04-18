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
from PyHSPlasma import *
from plasma.modifiers import ModBase

class ExampleModifier(bpy.types.operator):
    bl_idname = 'object.examplemodifier'
    bl_label = 'Example'
    category = 'Miscellaneous'
    
    @staticmethod
    def InitProperties():
        pass

    @staticmethod
    def Export():
        pass

    def execute(self, context):
        return {'FINISHED'}

def register():
    ExampleModifier.InitProperties()
    bpy.types.register(ExampleModifier)

def unregister():
    bpy.types.unregister(ExampleModifier)
