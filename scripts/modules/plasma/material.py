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
from plasma import utils
import os
import subprocess
import hashlib

def SetLayerColorToBlMat(layer, material):
    dcolor = material.diffuse_color
    layer.runtime = hsColorRGBA(dcolor[0],dcolor[1],dcolor[2],1.0)
    layer.preshade = hsColorRGBA(dcolor[0],dcolor[1],dcolor[2],1.0)
    layer.ambient = hsColorRGBA.kBlack
    scolor = material.specular_color
    layer.specular = hsColorRGBA(scolor[0],scolor[1],scolor[2],1.0)
    return layer

def SetLayerFlagsAlpha(layer):
    if layer.state.blendFlags & hsGMatState.kBlendAddColorTimesAlpha:
        layer.state.blendFlags |= hsGMatState.kBlendAlphaAdd
    elif layer.state.blendFlags & hsGMatState.kBlendMult:
        layer.state.blendFlags |= hsGMatState.kBlendAlphaMult
    else:
        layer.state.blendFlags |= hsGMatState.kBlendAlpha
        
def SetLayerFlags(slot,layer,material):
    #blendflags
    if slot.blend_type == "ADD":
        layer.state.blendFlags |= hsGMatState.kBlendAddColorTimesAlpha
    elif slot.blend_type == "MULTIPLY":
        layer.state.blendFlags |= hsGMatState.kBlendMult
    elif slot.blend_type == "SUBTRACT":
        layer.state.blendFlags |= hsGMatState.kBlendSubtract
    #miscflags
    if material.type == "WIRE":
        layer.state.miscFlags |= hsGMatState.kMiscWireFrame


def ExportMaterial(rm, loc, material, vos):
    mat = hsGMaterial(material.name)
    rm.AddObject(loc,mat)
    config = utils.PlasmaConfigParser()
    for slot in material.texture_slots:
        if slot:
            texture = slot.texture
            if texture.type == "NONE": #if it has a none type at least it has a name to export it under
                layer = plLayer(texture.name)
                SetLayerFlags(slot,layer, material)
                SetLayerColorToBlMat(layer,material)
                rm.AddObject(loc,layer)
                mat.addLayer(layer.key)
            elif texture.type == "IMAGE":
                if texture.image.source == "FILE":
                    cachepath = config.get('Paths', 'texcachepath')
                    exepath = config.get('Paths', 'executablepath')
                    buildplmipmap_path = os.path.join(exepath, "buildplmipmap")
                    imagename = os.path.split(texture.image.filename)[1]
                    cachename = os.path.splitext(imagename)[0]
                    cachefilepathfull = os.path.join(cachepath,cachename)

                    mm = plMipmap(cachename)                    
                    imgsstream = hsFileStream()

                    mm = plMipmap(cachename)
                    imgsstream = hsFileStream()
                    files_exist = False
                    src_checksum = None
                    have_to_process = True
                    try:
                        open(cachefilepathfull)#this shouldn't create a memory leak
                        src_checksum = open(cachefilepathfull+"_src.md5")#this shouldn't create a memory leak                        
                        files_exist = True
                    except:
                        pass
                    if files_exist: #we still need to check the sum
                        srctex = open(texture.image.filename,"rb")
                        if hashlib.md5(srctex.read()).hexdigest() == src_checksum.read():
                            print("Texture %s is the same as last time"%imagename)
                            have_to_process = False
                        else:
                            print("Texture %s has been changed.  Recompressing..."%imagename)
                        srctex.close()
                        src_checksum.close()
                    if have_to_process:
                        #create checksum
                        src_checksum = open(cachefilepathfull+"_src.md5","w")
                        srctex = open(texture.image.filename,"rb")
                        src_checksum.write(hashlib.md5(srctex.read()).hexdigest())
                        srctex.close()
                        src_checksum.close()
                        #compress texture
                        compresstype = "DXT1"
                        if texture.use_alpha:
                            compresstype = "DXT5"
                        callstuff = [buildplmipmap_path, texture.image.filename, cachefilepathfull, "mipmap", compresstype]
                        print(callstuff)
                        subprocess.call(callstuff)

                    imgsstream.open(cachefilepathfull, fmRead)
                    mm.readData(imgsstream)
                    imgsstream.close()
                    rm.AddObject(loc,mm)
        
                    layer = plLayer(texture.name)
                    SetLayerFlags(slot,layer, material)
                    layer.texture = mm.key
                    SetLayerColorToBlMat(layer,material)
                    rm.AddObject(loc,layer)
                    mat.addLayer(layer.key)
                                         
    if len(mat.layers) == 0: #save the day with an autogenerated layer
        layer = plLayer("%s_auto_layer"%material.name)
        SetLayerColorToBlMat(layer,material)
        rm.AddObject(loc,layer)
        mat.addLayer(layer.key)
        
    vos.materials[material] = mat.key


