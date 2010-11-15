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
from plasma import headers
from plasma import physics
from plasma import modifiers
from plasma import world
from plasma import object

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
    bpy.types.PHYSICS_PT_softbody_field_weights,
    bpy.types.OBJECT_PT_constraints,
    bpy.types.BONE_PT_constraints
]


#maybe try to get this class moved to the object module
class PlasmaObjectSettings(bpy.types.IDPropertyGroup):
    physics = PointerProperty(attr = 'physics', type = physics.PlasmaPhysicsSettings)
    modifiers = CollectionProperty(attr = 'modifiers', type = modifiers.PlasmaModifierSettings)

    drawableoverride = BoolProperty(name="Drawable Override", default = False)
    activemodifier = IntProperty(attr = 'activemodifier', default = 0)
    isdrawable = BoolProperty(name="Is Drawable", default=True, description="Export drawable for this object")
    isdynamic = BoolProperty(name="Dynamic", default=False)

def disable_panels():
    unregister = bpy.types.unregister
    for cls in hide:
        unregister(cls)

def plRegister():
    bpy.types.Object.plasma_settings = PointerProperty(attr = 'plasma_settings',
                                                       type = PlasmaObjectSettings,
                                                       name = 'Plasma Settings',
                                                       description = 'Plasma Engine Object Settings')
    bpy.types.World.plasma_age = PointerProperty(attr = 'plasma_age',
                                                     type = world.PlasmaAgeSettings,
                                                     name = 'Plasma Settings',
                                                     description = 'Plasma Engine Object Settings')
    
    bpy.types.Scene.plasma_page = PointerProperty(attr = 'plasma_page',
                                                       type = world.PlasmaPageSettings,
                                                       name = 'Plasma Settings',
                                                       description = 'Plasma Engine Object Settings')

    disable_panels()
    headers.register()
    modifiers.register()
    geometry.register()
    physics.register()
    world.register()
    object.register()
