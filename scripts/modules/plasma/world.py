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
import random

randomint = random.randint(100, 20000)
class AgeSettings(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "world"
    bl_label = "Plasma Age"
    def InitProperties():
        bpy.types.World.PointerProperty(attr="plasma_settings", type=bpy.types.PlasmaSettings, name="Plasma Settings", description="Plasma Engine Object Settings")
        
        bpy.types.PlasmaSettings.StringProperty(attr="agename", name="Age Name")
        bpy.types.PlasmaSettings.IntProperty(attr="ageprefix", name="Unique Age Prefix", default=100, soft_min=0, soft_max=20000)
        bpy.types.PlasmaSettings.EnumProperty(attr="plasmaversion",
                                  items=(
                                      ("PVPRIME", "Plasma 2.0 (59.11)", "Ages Beyond Myst, To D'ni, Untìl Uru"),
                                      ("PVPOTS", "Plasma 2.0 (59.12)", "Path of the Shell, Complete  Chronicles"),
                                      ("PVLIVE", "Plasma 2.0 (70.9)", "Myst Online: Uru Live, MOULagain, MagiQuest Online"),
                                      ("PVEOA", "Plasma 2.1", "End of Ages, Crowthistle"),
                                      ("PVHEX", "Plasma 3.0", "HexIsle")
                                  ),
                                  name="Plasma Version",
                                  description="Plasma Engine Version",
                                  default="PVPOTS")
        
        bpy.types.PlasmaSettings.BoolProperty(attr="advancedagesettings",name="Advanced Settings", default=False)
        
        bpy.types.PlasmaSettings.FloatProperty(attr="daylength", name="Day Length", default=24.0, soft_min=0.0)    
        bpy.types.PlasmaSettings.IntProperty(attr="startdaytime", name="Start Day Time", default=0, soft_min=0)
        bpy.types.PlasmaSettings.IntProperty(attr="maxcapacity", name="Max Capacity", default=150, soft_min=0, soft_max=1000)
        bpy.types.PlasmaSettings.IntProperty(attr="lingertime", name="Linger Time", default=180, soft_min=0)
        bpy.types.PlasmaSettings.IntProperty(attr="releaseversion", name="Release Version", default=0, soft_min=0)        
    InitProperties = staticmethod(InitProperties)
    def draw(self,context):
        layout = self.layout
        view = context.world
        pl = view.plasma_settings
        
        layout.prop(pl, "agename")
        layout.prop(pl, "plasmaversion")
        layout.prop(pl, "ageprefix")
        if pl.ageprefix == 100:
            layout.label(text="It looks like you haven't set your prefix.")
            layout.label(text="It is important that you set this to something other than the default.")
            layout.label(text="How about using this random number: %i"%randomint)
        layout.prop(pl, "advancedagesettings")
        if pl.advancedagesettings:
            layout.prop(pl, "daylength")
            layout.prop(pl, "startdaytime")
            layout.prop(pl, "maxcapacity")
            layout.prop(pl, "lingertime")
            layout.prop(pl, "releaseversion")

def register():
    AgeSettings.InitProperties()
    bpy.types.register(AgeSettings)

    
def unregister():
    bpy.types.unregister(AgeSettings)

