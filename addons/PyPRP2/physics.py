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
from . import utils

class PlasmaPhysicsSettings(bpy.types.IDPropertyGroup):
    enabled = BoolProperty(name="Physics Enabled", default=False)
    mass = FloatProperty(name="Mass",default=0.0,soft_min=0,soft_max=1000)
    friction = FloatProperty(name="Friction",default=0.5,soft_min=0,soft_max=10)
    restitution = FloatProperty(name="Restitution",default=0.0,soft_min=0.0,soft_max=1000)
    bounds = EnumProperty(
        items=(
            ("1", "Box", ""),
            ("2", "Sphere", ""),
            ("3", "Hull", ""),
            ("4", "Proxy", ""),
            ("5", "Explicit", ""),
            ("6", "Cylinder", "")
            ),
            name="Bounds Type",
            description="Bounds Type",
            default="3")
    subworld = StringProperty()
    sndgroup = StringProperty()
    radius = FloatProperty(name="Radius",default=1.0,soft_min=0,soft_max=10000)
    
class plPhysicalPanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "physics"
    bl_label = "Plasma Physical"

    def draw_header(self, context):
        view = context.object
        ph = view.plasma_settings.physics
        self.layout.prop(ph, "enabled", text="")

    def draw(self,context):
        layout = self.layout
        view = context.object
        ph = view.plasma_settings.physics
        layout.active = ph.enabled
        
        layout.prop(ph, "mass")
        layout.prop(ph, "friction")
        layout.prop(ph, "restitution")
        layout.label(text="SubWorld:")
        layout.prop(ph, "subworld")
        layout.label(text="Sound Group:")
        layout.prop(ph, "sndgroup")
        layout.label(text="Bounds Type:")
        layout.prop(ph, "bounds", text="")
        if ph.bounds == "2":
            layout.prop(ph, "radius")
        if ph.bounds not in ["2","4"]:
            layout.label(text="bounds type currently unsupported")

    @staticmethod
    def Export(rm,loc,blObj,so):
        plphysical = plGenericPhysical(blObj.name)
        plphysical.sceneNode = rm.getSceneNode(loc).key
        plphysical.object = so.key
        dynamic = blObj.plasma_settings.isdynamic
        kickable = dynamic and blObj.plasma_settings.physics.mass > 0
        if dynamic:
            pos = blObj.matrix_local.translation_part()
            plphysical.pos = hsVector3(pos[0], pos[1], pos[2])
            plphysical.memberGroup = plSimDefs.kGroupDynamic
        else:
            plphysical.pos = hsVector3(0.0, 0.0, 0.0)
            plphysical.memberGroup = plSimDefs.kGroupStatic
        plphysical.rot = hsQuat(0.0, 0.0, 0.0, 1.0)
        if kickable:
            plphysical.LOSDBs = 0x00
            plphysical.collideGroup |= (1 << plSimDefs.kGroupStatic)
            plphysical.collideGroup |= (1 << plSimDefs.kGroupDynamic)
            plphysical.collideGroup |= (1 << plSimDefs.kGroupAnimated)
        else:
            plphysical.LOSDBs = 0x44
        plphysical.mass = blObj.plasma_settings.physics.mass
        plphysical.friction = blObj.plasma_settings.physics.friction
        plphysical.restitution = blObj.plasma_settings.physics.restitution
        plphysical.boundsType = int(blObj.plasma_settings.physics.bounds)
        if plphysical.boundsType == plSimDefs.kSphereBounds: #sphere
             plphysical.radius = blObj.plasma_settings.physics.radius
        elif plphysical.boundsType == plSimDefs.kProxyBounds: #proxy
            plphysical.verts, plphysical.indices = BuildProxyBounds(blObj,dynamic) #do a little odd-looking compact python code
        rm.AddObject(loc,plphysical)
        return plphysical

def BuildProxyBounds(blObj, dynamic):
    if dynamic:
        mat = blObj.matrix_local.__copy__()
        mat[3] = [0,0,0,1.0] #translate to 0,0,0
    else:
        mat = blObj.matrix_local
        
    verts = []
    inds = []
    for face in blObj.data.faces:
        if len(face.vertices) == 3:
            inds.extend(face.vertices[:3])
        elif len(face.vertices) == 4:
            inds.extend(face.vertices[:3])
            inds.extend([face.vertices[0],face.vertices[2],face.vertices[3]])
    for vert in blObj.data.vertices:
        x,y,z = utils.transform_vector3_by_blmat((vert.co[0],vert.co[1],vert.co[2]),mat)
        verts.append(hsVector3(x,y,z))
    return verts, inds

def register():
    pass

def unregister():
    pass