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

import bpy,space_info
from bpy.props import *
from . import exporter
from . import importer

class INFO_MT_plasma(bpy.types.Menu):
    bl_idname = "INFO_MT_plasma"
    bl_label = "Plasma"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'EXEC_AREA'
        layout.operator_menu_enum("export.plasmaexport","type", text="Export")
        layout.operator_menu_enum("import.plasmaimport","type", text="Import")


class INFO_HT_header(space_info.INFO_HT_header):
    def draw(self, context):
        space_info.INFO_HT_header.draw(self,context)
        
        layout = self.layout
        sub = layout.row(align=True)
        sub.menu("INFO_MT_plasma")

def register():
    pass

    
def unregister():
    pass

