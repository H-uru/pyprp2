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

class MaintainerMarkerModifier(bpy.types.Operator):
    bl_idname = 'object.plmaintainermarkermodifier'
    bl_label = 'Maintainer\'s Marker'
    bl_description = 'GPS Coordinate Marker'
    category = 'Markers'

    __has_init = False

    @staticmethod
    def InitProperties(mod):
        mod.EnumProperty(
            attr="calibration",
            items = (
                ('broken', 'Random', 'Random coordinates'),
                ('repaired', 'Zeros', 'All zero coordinates'),
                ('calibrated', 'Calibrated', 'Working coordinates')
            ),
            name="Calibration",
            description="The type of coordinates generated.", 
            default='calibrated'
        )
        MaintainerMarkerModifier.__has_init = True

    @staticmethod
    def Export(ob, mod):
        pass

    def poll(self, context):
        return context.active_object

    def execute(self, context):
        ob = context.object
        pl = ob.plasma_settings
        mod = pl.modifiers.add()
        if not MaintainerMarkerModifier.__has_init:
            MaintainerMarkerModifier.InitProperties(mod)
        mod.name = ob.name
        mod.modclass = MaintainerMarkerModifier.bl_idname.split('.')[1]
        return {'FINISHED'}

class MaintainerMarkerModPanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'constraint'
    bl_label = 'GPS Coordinates'

    def poll(self, context):
        ob = context.active_object
        if not ob is None:
            pl = ob.plasma_settings
            if len(pl.modifiers) > 0:
                return pl.modifiers[pl.activemodifier].modclass == MaintainerMarkerModifier.bl_idname.split('.')[1]
        return False

    def draw(self, context):
        layout = self.layout
        
        ob = context.active_object
        pl = ob.plasma_settings
        plmod = pl.modifiers[pl.activemodifier]
        layout.label("Calibration Mode:")
        layout.row().prop(plmod, "calibration", expand=True)

def register():
    bpy.types.register(MaintainerMarkerModifier)
    bpy.types.register(MaintainerMarkerModPanel)

    return [MaintainerMarkerModifier]

def unregister():
    bpy.types.unregister(MaintainerMarkerModifier)
    bpy.types.unregister(MaintainerMarkerModPanel)
