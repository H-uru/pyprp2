import bpy
from PyHSPlasma import *
from plasma import utils


def CalculateCutoff(halfdist,AttenConstant,AttenLinear,AttenQuadratic):
    distance = halfdist #we start here and go up
    cutoff = 0.001 #when the lamp is this dim, we cut it off
    value = 1/(AttenConstant + AttenLinear*distance + AttenQuadratic*(distance**2))
    step = 2.0 #step 2.0 units in distance
    while value > 0.001:
        distance+=step
        value = 1/(AttenConstant + AttenLinear*distance + AttenQuadratic*(distance**2))
    return distance


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

        if lamp.sphere:
            print("  Sphere cutoff mode at %f" % lamp.distance)
            light.attenCutoff = Dist
        else:
            print("  Long-range cutoff")
            light.attenCutoff = CalculateCutoff(lamp.distance,light.attenConst,light.attenLinear,light.attenQuadratic)
    else:
        raise Exception("Unsupported Lamp Type")
    #do stuff that's needed for every type of light
    light.owner = sceneobject.key
    light.sceneNode = rm.getSceneNode(loc).key
    # Determine negative lighting....
    if lamp.negative:
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
    if lamp.diffuse:
        print("  Diffuse Lighting Enabled")
        light.diffuse=hsColorRGBA(R*energy,G*energy,B*energy,1.0)
    else:
        print("  Diffuse Lighting Disabled")
        light.diffuse=hsColorRGBA(0.0,0.0,0.0,1.0)


    # Specular
    if lamp.specular:
        print("  Specular Lighting Enabled")
        light.specular=hsColorRGBA(R*energy,G*energy,B*energy,1.0)
    else:
        print("  Specular Lighting Disabled")
        light.specular=hsColorRGBA(0.0,0.0,0.0,1.0)

    # Ambient:
    # Light not directly emitted by the light source, but present because of it.

    # If one wants to use a lamp as ambient, disable both diffuse and specular colors
    # Else, it's just set to 0,0,0 aka not used.

    if not lamp.specular and not lamp.diffuse:
        print("  Lamp is set as ambient light")
        light.ambient = hsColorRGBA(R * energy, G * energy, B * energy,1.0)
    else:
        light.ambient = hsColorRGBA(0.0, 0.0, 0.0, 0.0)

    #matrix fun
    l2w = utils.blMatrix44_2_hsMatrix44(blObj.matrix)
    light.lightToWorld = l2w
    matcopy = blObj.matrix.__copy__()
    matcopy.invert()
    w2l = utils.blMatrix44_2_hsMatrix44(matcopy)
    light.worldToLight = w2l
    
    rm.AddObject(loc,light)
    return light
