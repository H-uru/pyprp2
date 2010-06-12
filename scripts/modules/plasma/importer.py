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
import Mathutils
import os
from PyHSPlasma import *
from bpy.props import *
from plasma.utils import PlasmaConfigParser

ignore_book_and_print = True
bone_exclude_list = ["BookHandle", "Print_Trunk", "Bone_BookHinge1","Bone_BookHinge2","Print_L Foot","Print_R Foot","Print_L Hand","Print_R Hand",]

class PlasmaImport(bpy.types.Operator):
    bl_idname = "export.plasmaimport"
    bl_label = "Plasma Import"
    type = EnumProperty(items=(
                                  ("arm_f", "Female Armature", ""),
                                  ("arm_m", "Male Armature", "")
                              ),
                              name="Import Type",
                              description="Import Type")
    def execute(self, context):
        cfg = PlasmaConfigParser()
        importpath = cfg.get('Paths', 'importpath')
        if self.properties.type == "arm_f":
            importAvatarArmatureSystem(os.path.join(importpath,"GlobalAvatars_District_Female.prp"))
        elif self.properties.type == "arm_m":
            importAvatarArmatureSystem(os.path.join(importpath,"GlobalAvatars_District_Male.prp"))
        return {'FINISHED'}


def importAvatarArmatureSystem(path):
    Locations = {}
    sceneObjects = []
    bpy.ops.object.armature_add()
    blArm_obj = bpy.context.scene.objects.active
    blArm_obj.name = "PlasmaArmature"
    blArm = blArm_obj.data
    blArm.name = "PlasmaArmature"
    bpy.ops.object.mode_set(mode='EDIT')

    #clear out the default bone
    blArm.edit_bones.remove(blArm.edit_bones[0])

    #read the prp file
    rm = plResManager()
    page = rm.ReadPage(path)
    node = rm.getSceneNode(page.location)
    for soref in node.sceneObjects:
        if ignore_book_and_print:
            if soref.name.startswith("Bone_") and soref.name not in bone_exclude_list:
               obj = plSceneObject.Convert(soref.object)
               sceneObjects.append(obj)
               bone_importSOAndInterfaces(obj,blArm,Locations)
        else:
            if soref.name.startswith("Bone_") and soref.name in bone_exclude_list:
                obj = plSceneObject.Convert(soref.object)
                sceneObjects.append(obj)
                bone_importSOAndInterfaces(obj,blArm,Locations)

    for obj in sceneObjects:
        processBone(obj,blArm,Locations)
    bpy.ops.object.mode_set(mode='OBJECT')

def processBone(obj,blArm,Locations):
    if obj.coord and obj.coord.object:
        coordiface = plCoordinateInterface.Convert(obj.coord.object)
        hereloc = Mathutils.Vector(Locations[obj.key.name][0],Locations[obj.key.name][1],Locations[obj.key.name][2])
        blbone = blArm.edit_bones[obj.key.name]
        blbone.head = hereloc
        blbone.connected = True
        if blbone.head == hereloc:
            blbone.tail = Mathutils.Vector(hereloc[0],hereloc[1],hereloc[2]+1)
        else:
            blbone.tail = hereloc
        for child in coordiface.children:
            if not (ignore_book_and_print and (child.name in bone_exclude_list or child.name.startswith("Print"))):
                blArm.edit_bones[child.name].head = hereloc
                blArm.edit_bones[child.name].parent = blArm.edit_bones[obj.key.name]

def bone_importSOAndInterfaces(obj,blArm,Locations):
    if obj.coord and obj.coord.object:
        bpy.ops.armature.bone_primitive_add(name = obj.key.name)
        coordiface = plCoordinateInterface.Convert(obj.coord.object)
        Locations[obj.key.name] = (coordiface.localToWorld.mat[0][3],coordiface.localToWorld.mat[1][3],coordiface.localToWorld.mat[2][3])



 

        
