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

"Plasma Engine Environment"

import bpy,properties_data_modifier,space_info
import plasma

fullscreen = (lambda self, context: self.layout.operator("wm.window_fullscreen_toggle", icon='FULLSCREEN_ENTER', text=""))
     
def register():
    bpy.types.unregister(space_info.INFO_HT_header)
    plasma.plRegister()

def unregister():
    bpy.types.unregister(INFO_MT_plasma)
