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
import os
import configparser
from plasma import headers
from plasma import physics
from plasma import modifiers
from plasma import world

hide = [
    bpy.types.CLOTH_MT_presets,
    bpy.types.PHYSICS_PT_cloth,
    bpy.types.PHYSICS_PT_cloth_cache,
    bpy.types.PHYSICS_PT_cloth_collision,
    bpy.types.PHYSICS_PT_cloth_stiffness,
    bpy.types.PHYSICS_PT_cloth_field_weights,
    bpy.types.PHYSICS_PT_field,
    bpy.types.PHYSICS_PT_collision,
    bpy.types.PHYSICS_PT_fluid,
    bpy.types.PHYSICS_PT_domain_gravity,
    bpy.types.PHYSICS_PT_domain_boundary,
    bpy.types.PHYSICS_PT_domain_particles,
    bpy.types.PHYSICS_PT_smoke,
    bpy.types.PHYSICS_PT_smoke_field_weights,
    bpy.types.PHYSICS_PT_smoke_cache,
    bpy.types.PHYSICS_PT_smoke_highres,
    bpy.types.PHYSICS_PT_smoke_groups,
    bpy.types.PHYSICS_PT_smoke_cache_highres,
    bpy.types.PHYSICS_PT_softbody,
    bpy.types.PHYSICS_PT_softbody_cache,
    bpy.types.PHYSICS_PT_softbody_goal,
    bpy.types.PHYSICS_PT_softbody_edge,
    bpy.types.PHYSICS_PT_softbody_collision,
    bpy.types.PHYSICS_PT_softbody_solver,
    bpy.types.PHYSICS_PT_softbody_field_weights
    
##    bpy.types.MATERIAL_PT_context_material,
##    #bpy.types.MATERIAL_PT_preview,
##    bpy.types.MATERIAL_PT_diffuse,
##    bpy.types.MATERIAL_PT_specular,
##    bpy.types.MATERIAL_PT_shading,
##    bpy.types.MATERIAL_PT_transp,
##    bpy.types.MATERIAL_PT_mirror,
##    bpy.types.MATERIAL_PT_sss,
##    bpy.types.MATERIAL_PT_halo,
##    bpy.types.MATERIAL_PT_flare,
##    bpy.types.MATERIAL_PT_physics,
##    bpy.types.MATERIAL_PT_strand,
##    bpy.types.MATERIAL_PT_options,
##    bpy.types.MATERIAL_PT_shadow,
##    bpy.types.MATERIAL_PT_transp_game,
##
##    bpy.types.MATERIAL_MT_sss_presets,
##    bpy.types.MATERIAL_MT_specials,
##
##    bpy.types.MATERIAL_PT_volume_density,
##    bpy.types.MATERIAL_PT_volume_shading,
##    bpy.types.MATERIAL_PT_volume_lighting,
##    bpy.types.MATERIAL_PT_volume_transp,
##
##    bpy.types.MATERIAL_PT_volume_integration,
##
##    bpy.types.MATERIAL_PT_custom_props
]


class PlasmaSettings(bpy.types.IDPropertyGroup):
    pass

class PlasmaConfigParser(configparser.ConfigParser):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(PlasmaConfigParser, cls).__new__(cls, *args, **kwargs)
            cls.__instance.read(os.path.join(bpy.utils.home_paths()[1], 'pyprp2.conf'))
        return cls.__instance


def disable_panels():
    unregister = bpy.types.unregister
    for cls in hide:
        unregister(cls)

def plRegister():
    #print("plNetMsgPong!")
    disable_panels()
    bpy.types.register(PlasmaSettings)
    headers.register()
    modifiers.register()
    physics.register()
    world.register()

