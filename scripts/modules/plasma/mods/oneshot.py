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

__has_init = False


class OneShotMod(bpy.types.Operator):
    bl_idname = 'object.ploneshotmod'
    bl_label = 'One Shot'
    category = 'Avatar'

    @staticmethod
    def InitProperties(mod):
        mod.StringProperty(attr="animation", name="Animation", default="")
        mod.FloatProperty(attr="seekduration", name="Seek Duration", default=0.0,soft_min=0)
        mod.BoolProperty(attr="drivable", name="Drivable", default=False)
        mod.BoolProperty(attr="smartseek", name="Smart Seek", default=False)
        mod.BoolProperty(attr="reversable", name="Reversable", default=False)
        mod.BoolProperty(attr="noseek", name="No Seek", default=False)
        
    @staticmethod
    def Export(rm, so, mod):
        OneShotMod.InitProperties(mod) #just re-init them to make sure
        oneshotmod = plOneShotMod(mod.name)
        oneshotmod.animName = mod.animation
        oneshotmod.seekDuration = mod.seekduration
        oneshotmod.drivable = mod.drivable
        oneshotmod.smartSeek = mod.smartseek
        oneshotmod.reversable = mod.reversable
        oneshotmod.noSeek = mod.noseek
        rm.AddObject(so.key.location, oneshotmod)
        so.addModifier(oneshotmod.key)

    def execute(self, context):
        ob = context.object
        pl = ob.plasma_settings
        mod = pl.modifiers.add()
        mod.name = ob.name
        mod.modclass = OneShotMod.bl_idname.split('.')[1]
        return {'FINISHED'}
    

        
class OneShotModPanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'constraint'
    bl_label = 'One Shot Modifier'

    @classmethod
    def poll(self, context):
        ob = context.active_object
        if not ob is None:
            pl = ob.plasma_settings
            if len(pl.modifiers) > 0:
                return pl.modifiers[pl.activemodifier].modclass == OneShotMod.bl_idname.split('.')[1]
        return False

    def draw(self, context):
        layout = self.layout
        
        ob = context.active_object
        pl = ob.plasma_settings
        plmod = pl.modifiers[pl.activemodifier]
        try:
            plmod.animation #see if the structure is inited yet
        except:
            OneShotMod.InitProperties(plmod)

        layout.prop(plmod, "animation")
        layout.prop(plmod, "seekduration")

        layout.prop(plmod, "drivable")
        layout.prop(plmod, "smartseek")
        layout.prop(plmod, "reversable")
        layout.prop(plmod, "noseek")

def register():
    bpy.types.register(OneShotMod)
    bpy.types.register(OneShotModPanel)
    return [OneShotMod]

def unregister():
    bpy.types.unregister(OneShotMod)
    bpy.types.unregister(OneShotModPanel)
