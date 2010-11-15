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
from plasma import material
from plasma.utils import PlasmaConfigParser

alpha_names = ['alpha', 'Alpha']
colour_names = ['colour', 'color', 'col', 'Colour', 'Color', 'Col']

def AverageRGB(cols):
    return (cols[0] + cols[1] + cols[2]) / 3.0

def DigestBlMesh(mesh): #Let's hope for no indigestion.
#loop through all the faces and create a pointer-based face-list ([vert0,vert1,vert2,vert3,vert4,vert5] would be two faces) to corresponding verts (vertlist is the same len as facelist)
#condense vert-list based on copies. Re-adress the faces on the way.
    col_lay = list(set(mesh.vertex_colors.keys()) & set(colour_names)) or ['']
    vertex_color = mesh.vertex_colors.get(col_lay[0])
    alpha_lay = list(set(mesh.vertex_colors.keys()) & set(alpha_names)) or ['']
    vertex_alpha = mesh.vertex_colors.get(alpha_lay)
    
    inds_by_material = {}
    #create empty arrays for the face inds (pointers)
    if len(mesh.materials) < 1:
        raise Exception("Object with meah %s does not have a material"%mesh.name)
    for mati in range(len(mesh.materials)):
        inds_by_material[mati] = []

#system: dict[blvertind][positions of uvs] = plGBufferVertex
#go through faces and connect and grow dict.  Then, dump plvert instances into a big list.

    plasma_vert_dict = {}
    for i, face in enumerate(mesh.faces):
        matidx = face.material_index
        face_uvs = []
        for uvtex in mesh.uv_textures:
            face_uvs.append((uvtex.data[i].uv1, uvtex.data[i].uv2, uvtex.data[i].uv3, uvtex.data[i].uv4))
        #handle vertex colors
        if vertex_color:
            cols = (vertex_color.data[i].color1, vertex_color.data[i].color2, vertex_color.data[i].color3, vertex_color.data[i].color4)
        else:
            cols = ((1.0,1.0,1.0), (1.0,1.0,1.0), (1.0,1.0,1.0), (1.0,1.0,1.0))
        #handle vertex alpha
        if vertex_alpha:
            vtx_alphas = (AverageRGB(vertex_alpha.data[i].color1), AverageRGB(vertex_alpha.data[i].color2), AverageRGB(vertex_alpha.data[i].color3), AverageRGB(vertex_alpha.data[i].color4))
        else:
            vtx_alphas = (1.0, 1.0, 1.0, 1.0)
        temp_vert_instances = []
        for j, vertidx in enumerate(face.verts):
            #find or create vertex
            secondkey = tuple([(face_uvs[uvi][j][0],1.0-face_uvs[uvi][j][1]) for uvi in range(len(mesh.uv_textures))])
            first_item = plasma_vert_dict.get(vertidx)
            vertex = None
            if first_item:
                vertex = first_item.get(secondkey)
            else:
                plasma_vert_dict[vertidx] = {}
            if vertex == None:
                #darn, we have to create the vert
                vert = mesh.verts[vertidx]
                plvert = plGBufferVertex()
                plvert.pos = hsVector3(vert.co[0],vert.co[1],vert.co[2]) #position
                plvert.normal = hsVector3(vert.normal[0],vert.normal[1], vert.normal[2]) #normal
                plvert.UVWs = [hsVector3(face_uvs[uvi][j][0],1.0-face_uvs[uvi][j][1],0.0) for uvi in range(len(mesh.uv_textures))]
                vcolor = cols[j]

                plvert.color = hsColor32(int(round(vcolor[0]*255)), int(round(vcolor[1]*255)), int(round(vcolor[2]*255)), int(round(vtx_alphas[j]*255))).color

                plasma_vert_dict[vertidx][secondkey] = plvert
                vertex=plvert
            temp_vert_instances.append(vertex)
                

        if len(temp_vert_instances) == 3:
            inds_by_material[matidx].extend([temp_vert_instances[0],
                                             temp_vert_instances[1],
                                             temp_vert_instances[2]])      
        elif len(temp_vert_instances) == 4: # a quad must be separated into two triangles
            inds_by_material[matidx].extend([temp_vert_instances[0],
                                             temp_vert_instances[1],
                                             temp_vert_instances[2]])  # first triangle
            inds_by_material[matidx].extend([temp_vert_instances[0],
                                             temp_vert_instances[2],
                                             temp_vert_instances[3]])  # second triangle

    bufferverts = []
    for item1 in plasma_vert_dict.values():
        for item2 in item1.values():
            bufferverts.append(item2)
    return bufferverts,inds_by_material

def GetPlasmaVertsIndsBoundsByMaterial(bufferverts, inds_by_material, material_index):
    pointerinds = inds_by_material[material_index]
    material_owned_verts = []
    lboundsmin=None # maximum vertex
    lboundsmax=None # minimum vertex
    #separate the verts
    for ptrind in pointerinds:
        if ptrind not in material_owned_verts: #if it's not there already.
            material_owned_verts.append(ptrind)

    for vert in material_owned_verts: #we don't need the blvert keying here
        #sneak some bounds creation in here
        vertpos = vert.pos
        if lboundsmin is None or lboundsmax is None:
            lboundsmin = [vertpos.X,vertpos.Y,vertpos.Z]
            lboundsmax = [vertpos.X,vertpos.Y,vertpos.Z]
        else:
            #the min
            if vertpos.X < lboundsmin[0]:
                lboundsmin[0] = vertpos.X
            if vertpos.Y < lboundsmin[1]:
                lboundsmin[1] = vertpos.Y
            if vertpos.Z < lboundsmin[2]:
                lboundsmin[2] = vertpos.Z
            #now the max
            if vertpos.X > lboundsmax[0]:
                lboundsmax[0] = vertpos.X
            if vertpos.Y > lboundsmax[1]:
                lboundsmax[1] = vertpos.Y
            if vertpos.Z > lboundsmax[2]:
                lboundsmax[2] = vertpos.Z
    if lboundsmin is None or lboundsmax is None:
        lboundsmin = [0.0,0.0,0.0]
        lboundsmax = [0.0,0.0,0.0]
    inds = []
    for ind in pointerinds:
        inds.append(material_owned_verts.index(ind))
    return material_owned_verts, inds, (lboundsmin,lboundsmax)

def CreateDSpansName(agename, pagename, renderlevel, criteria):
    spanlabel = "Spans"
    if renderlevel > 0: #it's a blend
        spanlabel = "BlendSpans"
    one="%08x" % renderlevel
    two="%x" % criteria
    name = "%s_District_%s_%08x_%x%s"%(agename, pagename, renderlevel, criteria, spanlabel)
    return name
    
def CreateDrawableSpans(agename,scenenode,renderlevel,criteria,pagename,passindex):
    name = CreateDSpansName(agename, pagename, renderlevel, criteria)+passindex
    dspans = plDrawableSpans(name)
    dspans.sceneNode = scenenode.key
    dspans.renderLevel = renderlevel
    dspans.criteria = criteria
    return dspans

class BufferGroupInfo:
    def __init__(self):
        self.verts_to_be_written = []
        self.inds_to_be_written = []

class GeometryManager: #this could be passed all the stuff needed to make dspans
    def __init__(self, agename, pagename):
        self.dspans_list = []
        self.agename = agename
        self.pagename = pagename

    def AddDrawableSpans(self, dspans):
        self.dspans_list.append([dspans,[]]) #dspans and buffergroup list
        return len(self.dspans_list)-1
    
    def FindOrCreateBufferGroup(self, dspansind, UVCount,num_vertexs):
        if num_vertexs >= 0x8000:
            raise Exception("Too many verts.")
        dspans,buffergroupinfos = self.dspans_list[dspansind]
        for idx in range(len(dspans.bufferGroups)):
            bufferGroup=dspans.bufferGroups[idx]
            if bufferGroup.numUVs==UVCount and len(buffergroupinfos[idx].verts_to_be_written)+num_vertexs < 0x8000:
                return idx
        #not found - create a new bufferGroup with the required format
        bgformat = 0
        bgformat = bgformat | (UVCount & plGBufferGroup.kUVCountMask)
        bufferGroupInd = dspans.createBufferGroup(bgformat)
        bginfo = BufferGroupInfo()
        buffergroupinfos.append(BufferGroupInfo())
        # and return new index in list
        return bufferGroupInd

    def FindOrCreateDrawableSpans(self, rm, loc, renderlevel, criteria, passindex): #returns dspans ind
        name = CreateDSpansName(self.agename, self.pagename, renderlevel, criteria)+passindex
        for i in range(len(self.dspans_list)):
            dspans = self.dspans_list[i]
            if dspans[0].key.name == name:
                return i
        dspans = CreateDrawableSpans(self.agename,rm.getSceneNode(loc),renderlevel,criteria,self.pagename, passindex)
        rm.AddObject(loc,dspans)
        return self.AddDrawableSpans(dspans)


    def FinallizeDSpans(self,dspansind):
        dspans,buffergroupinfos = self.dspans_list[dspansind]
        for bgidx, bginfo in enumerate(buffergroupinfos):
            bg = dspans.bufferGroups[bgidx]
            bg.addVertices(bginfo.verts_to_be_written) #NOT bginfo.verts_to_be_writtens
            bg.addIndices(bginfo.inds_to_be_written)
            
            print("Creating Cell with the length of %i verts in buffer %i"%(len(bginfo.verts_to_be_written),bgidx))
            cell = plGBufferCell()
            cell.vtxStart = 0
            cell.colorStart = -1
            cell.length = len(bginfo.verts_to_be_written)
            bg.addCells([cell])

    def FinallizeAllDSpans(self):
        for i in range(len(self.dspans_list)):
            self.FinallizeDSpans(i)
            
    def AddBlenderMeshToDSpans(self, dspansind, blObj, hasCI, vos):
        material_keys = vos.materials
        light_keys = vos.lights
        mesh = blObj.data
        hasvtxalpha = (set(mesh.vertex_colors.keys()) & set(alpha_names) != set())
        dspans,buffergroupinfos = self.dspans_list[dspansind]
        bufferverts,inds_by_material = DigestBlMesh(mesh)
        icicle_inds = []
    
        for matindex in inds_by_material:
            print("Adding geometry associated with %s"%mesh.materials[matindex].name)
            verts, inds, bounds = GetPlasmaVertsIndsBoundsByMaterial(bufferverts, inds_by_material, matindex)
            print("  Bounds:",bounds)
            print("  Verts: %i"%len(verts))
            print("  UVW layers: %i"%len(mesh.uv_textures))
            buffergroup_index = self.FindOrCreateBufferGroup(dspansind,len(mesh.uv_textures),len(verts))
            print("  Buffer Group Index: %i"%buffergroup_index)
            bg = dspans.bufferGroups[buffergroup_index]
            
            vert_offset = len(buffergroupinfos[buffergroup_index].verts_to_be_written)
            inds_offset = len(buffergroupinfos[buffergroup_index].inds_to_be_written)
            buffergroupinfos[buffergroup_index].verts_to_be_written.extend(verts)
            buffergroupinfos[buffergroup_index].inds_to_be_written.extend([i+vert_offset for i in inds])
            #create our icicle
            ice = plIcicle()
            #transformations
            if hasCI:
                #just put some identities in
                ice.localToWorld = hsMatrix44()
                ice.worldToLocal = hsMatrix44()
            else:
                #we need the transform
                l2w = utils.blMatrix44_2_hsMatrix44(blObj.matrix)
                ice.localToWorld = l2w
                matcopy = blObj.matrix.__copy__()
                matcopy.invert()
                w2l = utils.blMatrix44_2_hsMatrix44(matcopy)
                ice.worldToLocal = w2l
            #bounds stuff
            #local bounds, the easy ones
            lbounds = hsBounds3Ext()
            lbounds.mins = hsVector3(bounds[0][0],bounds[0][1],bounds[0][2])
            lbounds.maxs = hsVector3(bounds[1][0],bounds[1][1],bounds[1][2])
            lbounds.flags = hsBounds3Ext.kAxisAligned
            ice.localBounds = lbounds
            #world bounds, slightly harder
            wbounds = hsBounds3Ext()
            minwbounds = utils.transform_vector3_by_plmat(bounds[0], ice.localToWorld)
            maxwbounds = utils.transform_vector3_by_plmat(bounds[1], ice.localToWorld)
            wbounds.mins = hsVector3(minwbounds[0],minwbounds[1],minwbounds[2])
            wbounds.maxs = hsVector3(maxwbounds[0],maxwbounds[1],maxwbounds[2])
            wbounds.flags = hsBounds3Ext.kAxisAligned
            ice.worldBounds = wbounds
            #buffergroup stuff
            ice.groupIdx = buffergroup_index
            ice.VLength = len(verts)
            ice.VStartIdx = vert_offset
            ice.ILength = len(inds)
            ice.IStartIdx = inds_offset
            #find or create material
            matkey = material_keys[mesh.materials[matindex]]
            if matkey in dspans.materials:
                print("Already have it.")
            else:
                dspans.addMaterial(matkey)
            ice.materialIdx = dspans.materials.index(matkey)
            #set flags
            if hasvtxalpha:
                ice.props |= plSpan.kLiteVtxNonPreshaded
                #start of some hacky stuff
                gmat = hsGMaterial.Convert(matkey.object)
                for layerkey in gmat.layers:
                    layer = plLayerInterface.Convert(layerkey.object)
                    material.SetLayerFlagsAlpha(layer)
            #lights
            blmat = mesh.materials[matindex]
            if not blmat.shadeless:
                ice.props |= plSpan.kPropHasPermaLights
                for lightkey in light_keys.values(): #to do: check for lightgroup
                    print("Appending light %s"%lightkey.name)
                    ice.addPermaLight(lightkey)
            #finish up
            dspans.addIcicle(ice)
            icicle_inds.append(len(dspans.spans)-1)
        #deal with the DIIndex
        di_ind_obj = plDISpanIndex()
        di_ind_obj.indices = icicle_inds
        dspans.addDIIndex(di_ind_obj)
        return dspans,(len(dspans.DIIndices)-1)

class AdvRenderLevelPanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_label = 'Render Flags'

    @classmethod
    def poll(self, context):
        cfg = PlasmaConfigParser()
        if cfg.getboolean('Advanced', 'iamyeesha'):
            return context.mesh
        return False

    def draw(self, context):
        layout = self.layout
        ob = context.object

        row = layout.row()
        col = row.column()
        col.label(text = 'Major')
        col.label(text = 'Opaque')
        col.label(text = 'FB')
        col.label(text = 'DefRend')
        col.label(text = 'Blend')
        col.label(text = 'Late')

        col = row.column()
        col.label(text = 'Minor')
        col.label(text = 'Opaque')
        col.label(text = 'FB')
        col.label(text = 'DefRend')
        col.label(text = 'Blend')
        col.label(text = 'Late')

        layout.label(text = 'DANGER! This will likely cause rendering errors in Plasma!')
        layout.prop(ob.plasma_settings, 'drawableoverride')

def register():
    bpy.types.register(AdvRenderLevelPanel)

def unregister():
    bpy.types.unregister(AdvRenderLevelPanel)
