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
from . import utils


def ExportLamp(rm, loc, blObj, vos, sceneobject):
    lamp = blObj.data
    if lamp.type == "POINT":
        print(" [OmniLight]")
        light = plOmniLightInfo(blObj.name)
        Dist = lamp.distance
        if lamp.falloff_type == "LINEAR_QUADRATIC_WEIGHTED":
            print("  Linear Quadratic Attenuation")
            light.attenQuadratic = lamp.quadratic_attenuation/Dist
            light.attenLinear = lamp.linear_attenuation/Dist
            light.attenConst = 1.0
        else:
            print("  Linear Attenuation")
            light.attenQuadratic = 0.0
            light.attenLinear = 1.0/Dist
            light.attenConst = 1.0

        if lamp.use_sphere:
            print("  Sphere cutoff mode at %f" % lamp.distance)
            light.attenCutoff = Dist
        else:
            print("  Long-range cutoff")
            light.attenCutoff = Dist*2 #it should be about twice the half distance eg. (1+1/2+1/4+1/8+1/16)
    else:
        raise Exception("Unsupported Lamp Type")
    #do stuff that's needed for every type of light
    light.owner = sceneobject.key
    light.sceneNode = rm.getSceneNode(loc).key
    rm.AddObject(loc,light)
    # Determine negative lighting....
    if lamp.use_negative:
        print("  >>>Negative light<<<")
        R = 0.0 - lamp.color[0]
        G = 0.0 - lamp.color[1]
        B = 0.0 - lamp.color[2]
    else:
        R = lamp.color[0]
        G = lamp.color[1]
        B = lamp.color[2]

    # Plasma has the same Lights as DirectX:
    #

    energy = lamp.energy * 2

    # Diffuse:
    if lamp.use_diffuse:
        print("  Diffuse Lighting Enabled")
        light.diffuse=hsColorRGBA(R*energy,G*energy,B*energy,1.0)
    else:
        print("  Diffuse Lighting Disabled")
        light.diffuse=hsColorRGBA(0.0,0.0,0.0,1.0)


    # Specular
    if lamp.use_specular:
        print("  Specular Lighting Enabled")
        light.specular=hsColorRGBA(R*energy,G*energy,B*energy,1.0)
    else:
        print("  Specular Lighting Disabled")
        light.specular=hsColorRGBA(0.0,0.0,0.0,1.0)

    # Ambient:
    # Light not directly emitted by the light source, but present because of it.

    # If one wants to use a lamp as ambient, disable both diffuse and specular colors
    # Else, it's just set to 0,0,0 aka not used.

    if not lamp.use_specular and not lamp.use_diffuse:
        print("  Lamp is set as ambient light")
        light.ambient = hsColorRGBA(R * energy, G * energy, B * energy,1.0)
    else:
        light.ambient = hsColorRGBA(0.0, 0.0, 0.0, 0.0)

    #matrix fun
    l2w = utils.blMatrix44_2_hsMatrix44(blObj.matrix_local)
    light.lightToWorld = l2w
    matcopy = blObj.matrix_local.__copy__()
    matcopy.invert()
    w2l = utils.blMatrix44_2_hsMatrix44(matcopy)
    light.worldToLight = w2l
    return light



##Plasma Vert-Baking Code
##If someone thinks of a better place to put it, feel free to move it.

def set_vertex_color_black(vcol): #is there a better way?
    for i in vcol.data:
        i.color1 = (0,0,0)
        i.color2 = (0,0,0)
        i.color3 = (0,0,0)
        i.color4 = (0,0,0)

def add_colors(col1, col2):
    #if the value is over one it will be changed to one automatically when it is set
    return (col1[0]+col2[0],col1[1]+col2[1],col1[2]+col2[2])

def calc_color_omni(pllamp, distance, normal_dot):
    factor = (1/(pllamp.attenConst + pllamp.attenLinear*distance + pllamp.attenQuadratic*(distance**2)))*normal_dot
    return pllamp.diffuse.red*factor,pllamp.diffuse.green*factor,pllamp.diffuse.blue*factor

def light_mesh(mesh, matrix_world, pllamp, vpaint):
    #decide lighting function
    if pllamp.key.type == plFactory.kOmniLightInfo:
        lightfunc = calc_color_omni
    else:
        #unsupported type
        return

    l_pos = utils.hsMatrix44_2_blMatrix44(pllamp.lightToWorld).translation_part()
    for index_face, face in enumerate(mesh.faces):
        for index_v, vertexind in enumerate(face.vertices):
            v_pos = mesh.vertices[vertexind].co*matrix_world
            dot = mesh.vertices[vertexind].normal.dot((l_pos-v_pos).normalize())
            if dot < 0:
                continue
            dist = (v_pos-l_pos).length
            #very, very ugly
            if index_v == 0:
                vpaint.data[index_face].color1 = add_colors(vpaint.data[index_face].color1,lightfunc(pllamp, dist,dot))
            elif index_v == 1:
                vpaint.data[index_face].color2 = add_colors(vpaint.data[index_face].color2,lightfunc(pllamp, dist,dot))
            elif index_v == 2:
                vpaint.data[index_face].color3 = add_colors(vpaint.data[index_face].color3,lightfunc(pllamp, dist,dot))
            else:
                vpaint.data[index_face].color4 = add_colors(vpaint.data[index_face].color4,lightfunc(pllamp, dist,dot))
