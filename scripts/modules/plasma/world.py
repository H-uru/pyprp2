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
from PyHSPlasma import *
import random

randomint = random.randint(100, 20000)


class PlasmaAgeSettings(bpy.types.IDPropertyGroup):
    name = StringProperty(name='Age Name')
    prefix = IntProperty(name='Unique Age Prefix', default=100, soft_min=0, soft_max=20000)
    plasmaversion = EnumProperty(items=(
                                      ('PVPRIME', 'Plasma 2.0 (59.11)', 'Ages Beyond Myst, To D\'ni, Untìl Uru'),
                                      ('PVPOTS', 'Plasma 2.0 (59.12)', 'Path of the Shell, Complete  Chronicles'),
                                      ('PVLIVE', 'Plasma 2.0 (70.9)', 'Myst Online: Uru Live, MOULagain, MagiQuest Online'),
                                      ('PVEOA', 'Plasma 2.1', 'End of Ages, Crowthistle'),
                                      ('PVHEX', 'Plasma 3.0', 'HexIsle')
                                  ),
                                  name='Plasma Version',
                                  description='Plasma Engine Version',
                                  default='PVPOTS')
    isadvanced = BoolProperty(name='Advanced Settings', default=False)
    daylength = FloatProperty(name='Day Length', default=24.0, soft_min=0.0)    
    startdaytime = IntProperty(name='Start Day Time', default=0, soft_min=0)
    maxcapacity = IntProperty(name='Max Capacity', default=150, soft_min=0, soft_max=1000)
    lingertime = IntProperty(name='Linger Time', default=180, soft_min=0)
    releaseversion = IntProperty(name='Release Version', default=0, soft_min=0)
        
class PlasmaPageSettings(bpy.types.IDPropertyGroup):
    isexport = BoolProperty(name = 'Export', default = True, options = set(),
                        description = 'Export this scene to Plasma')
    load = BoolProperty(name = 'Load Scene', default = True, options = set(),
                        description = 'Load this scene when linking in')
    id = IntProperty(name = 'Scene Identifier', default = 0, min = 0,
                        options = set(), subtype = 'UNSIGNED', max = 240,
                        description = 'Unique numeric scene identifier')
    itinerant = BoolProperty(name = 'Intinerant', default = False, options = set(),
                        description = 'Do not unload this scene')

class plAgeSettingsPanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'world'
    bl_label = 'Plasma Age'

    def draw(self,context):
        layout = self.layout
        view = context.world
        pl = view.plasma_age
        
        layout.prop(pl, 'name')
        layout.prop(pl, 'plasmaversion')
        layout.prop(pl, 'prefix')
        if pl.prefix == 100:
            layout.label(text='It looks like you haven\'t set your prefix.')
            layout.label(text='It is important that you set this to something other than the default.')
            layout.label(text='How about using this random number: %i'%randomint)
        layout.prop(pl, 'isadvanced')
        if pl.isadvanced:
            layout.prop(pl, 'daylength')
            layout.prop(pl, 'startdaytime')
            layout.prop(pl, 'maxcapacity')
            layout.prop(pl, 'lingertime')
            layout.prop(pl, 'releaseversion')

class plPagePanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'
    bl_label = 'Plasma Scene'

    @classmethod
    def poll(self, context):
        return context.scene != None

    def draw_header(self, context):
        scn = context.scene
        self.layout.prop(scn.plasma_page, 'isexport', text = '')

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        pl = scn.plasma_page

        layout.enabled = pl.isexport

        row = layout.row()
        row.prop(scn, 'name')
        row.prop(pl, 'load')

        row = layout.row()
        col = row.column()
        col.prop(pl, 'id')
        col = row.column()
        col.row().label(text = 'Page Flags:')
        col.row().prop(pl, 'itinerant')

def register():
    bpy.types.register(plAgeSettingsPanel)
    bpy.types.register(plPagePanel)

def unregister():
    bpy.types.unregister(plAgeSettingsPanel)
    bpy.types.unregister(plPagePanel)
