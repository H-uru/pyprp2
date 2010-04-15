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
from plasma import utils

def BuildProxyBounds(blObj):
    verts = []
    inds = []
    for face in blObj.data.faces:
        if len(face.verts) == 3:
            inds.extend([face.verts[0],face.verts[1],face.verts[2]])
        elif len(face.verts) == 4:
            inds.extend([face.verts[0],face.verts[1],face.verts[2]])
            inds.extend([face.verts[0],face.verts[2],face.verts[3]])
    for vert in blObj.data.verts:
        x,y,z = utils.transform_vector3_by_blmat((vert.co[0],vert.co[1],vert.co[2]),blObj.matrix)
        verts.append(hsVector3(x,y,z))
    return verts, inds
    
class Physical(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "physics"
    bl_label = "Plasma Physical"
    def InitProperties():
        #I hope recreating this type isn't too much of a hit.  If there's a way to get context passed to the creator it could test for if it's there.
        bpy.types.Object.PointerProperty(attr="plasma_settings", type=bpy.types.PlasmaSettings, name="Plasma Settings", description="Plasma Engine Object Settings")
        
        bpy.types.PlasmaSettings.BoolProperty(attr="physicsenabled",name="Physics Enabled", default=False)
        bpy.types.PlasmaSettings.FloatProperty(attr="physicsmass",name="Mass",default=0.0,soft_min=0,soft_max=1000)
        bpy.types.PlasmaSettings.FloatProperty(attr="physicsfriction",name="Friction",default=0.0,soft_min=0,soft_max=10)
        bpy.types.PlasmaSettings.FloatProperty(attr="physicsrestitution",name="Restitution",default=-1.0,soft_min=-1.0,soft_max=1000)
        bpy.types.PlasmaSettings.EnumProperty(attr="physicsbounds",
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
        bpy.types.PlasmaSettings.StringProperty(attr="physicssubworld")
        bpy.types.PlasmaSettings.StringProperty(attr="physicssndgroup")
        bpy.types.PlasmaSettings.FloatProperty(attr="physicsradius",name="Radius",default=1.0,soft_min=0,soft_max=1000)
    InitProperties = staticmethod(InitProperties)
    def draw_header(self, context):
        view = context.object
        pl = view.plasma_settings
        self.layout.prop(pl, "physicsenabled", text="")

    def draw(self,context):
        layout = self.layout
        view = context.object
        pl = view.plasma_settings
        layout.active = pl.physicsenabled
        
        layout.prop(pl, "physicsmass")
        layout.prop(pl, "physicsfriction")
        layout.prop(pl, "physicsrestitution")
        layout.label(text="SubWorld:")
        layout.prop(pl, "physicssubworld")
        layout.label(text="Sound Group:")
        layout.prop(pl, "physicssndgroup")
        layout.label(text="Bounds Type:")
        layout.prop(pl, "physicsbounds", text="")
        if pl.physicsbounds == "2":
            layout.prop(pl, "physicsradius")
        if pl.physicsbounds not in ["2","4"]:
            layout.label(text="bounds type currently unsupported")

    def Export(rm,loc,blObj,so):
        plphysical = plGenericPhysical(blObj.name)
        plphysical.sceneNode = rm.getSceneNode(loc).key
        plphysical.object = so.key
        plphysical.category = 0x02000000
        plphysical.pos = hsVector3(0.0, 0.0, 0.0)
        plphysical.rot = hsQuat(0.0, 0.0, 1.0, 0.0)
        plphysical.LOSDBs = 0x44
        plphysical.mass = blObj.plasma_settings.physicsmass
        plphysical.friction = blObj.plasma_settings.physicsfriction
        plphysical.restitution = blObj.plasma_settings.physicsrestitution
        plphysical.boundsType = int(blObj.plasma_settings.physicsbounds)
        if plphysical.boundsType == plSimDefs.kSphereBounds: #sphere
             plphysical.radius = blObj.plasma_settings.physicsradius
        elif plphysical.boundsType == plSimDefs.kProxyBounds: #proxy
            plphysical.verts, plphysical.indices = BuildProxyBounds(blObj) #do a little odd-looking compact python code
        rm.AddObject(loc,plphysical)
        return plphysical
    Export = staticmethod(Export)

def register():
    Physical.InitProperties()
    bpy.types.register(Physical)

    
def unregister():
    bpy.types.unregister(Physical)
