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

class SpawnModifier(bpy.types.Operator):
    bl_idname = 'object.plspawnmodifier'
    bl_label = 'Link-In Point'
    bl_description = 'Starting point for a player'
    category = 'Avatar'

    @staticmethod
    def Export(rm, so, mod):
        spawnmod = plSpawnModifier(mod.name)
        so.addModifier(spawnmod.key)
        rm.AddObject(so.key.location, spawnmod)

    def execute(self, context):
        ob = context.object
        pl = ob.plasma_settings
        mod = pl.modifiers.add()
        mod.name = ob.name
        mod.modclass = SpawnModifier.bl_idname.split('.')[1]
        return {'FINISHED'}

def register():
    bpy.types.register(SpawnModifier)
    return [SpawnModifier]

def unregister():
    pass
