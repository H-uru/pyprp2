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

class plObject(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_label = "Plasma Object"
    def InitProperties():
        bpy.types.Object.PointerProperty(attr="plasma_settings", type=bpy.types.PlasmaSettings, name="Plasma Settings", description="Plasma Engine Object Settings")
        bpy.types.PlasmaSettings.BoolProperty(attr="isdrawable",name="Is Drawable", default=True, description="Export drawable for this object")
    def draw(self,context):
        layout = self.layout
        view = context.object
        pl = view.plasma_settings
        self.layout.prop(pl, "isdrawable")

def register():
    plObject.InitProperties()
    bpy.types.register(plObject)

    
def unregister():
    bpy.types.unregister(plObject)

