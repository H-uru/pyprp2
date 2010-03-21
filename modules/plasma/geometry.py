import bpy
from PyHSPlasma import *


def DigestBlMesh(mesh): #Let's hope for no indigestion.
    vertex_color = mesh.vertex_colors.get("Col")
    vertex_alpha = mesh.vertex_colors.get("Alpha")
    
    inds_by_material = {}
    #create empty arrays for the face inds (pointers)
    if len(mesh.materials) < 1:
        raise Exception("Object with meah %s does not have a material"%mesh.name)
    for mati in range(len(mesh.materials)):
        inds_by_material[mati] = []

    bufferverts = {} #keyed by blender verts
    for vert in mesh.verts:
        #create our lookup and fill in what we can
        #the rest of this function will focus on filling in the gaps in our data
        vertcols = [] #we'll get the mean of all the different colors of a single vertex at the end
        claimed_by_these_materials = []
        v = plGBufferVertex()
        #position
        v.pos = hsVector3(vert.co[0],vert.co[1],vert.co[2])
        #normal
        v.normal = hsVector3(vert.normal[0],vert.normal[1], vert.normal[2])
        #add the stuff to the dict
        bufferverts[vert] = [v,vertcols,claimed_by_these_materials]
    for i, face in enumerate(mesh.faces):
        matidx = face.material_index
        face_uvs = []
        for uvtex in mesh.uv_textures:
            face_uvs.append((uvtex.data[i].uv1, uvtex.data[i].uv2, uvtex.data[i].uv3, uvtex.data[i].uv4))
        col = (vertex_color.data[i].color1, vertex_color.data[i].color2, vertex_color.data[i].color3, vertex_color.data[i].color4)
        #store face as pointers to the Plasma verts
        if len(face.verts) == 3:
            inds_by_material[matidx].extend([bufferverts[mesh.verts[face.verts[0]]][0],
                                             bufferverts[mesh.verts[face.verts[1]]][0],
                                             bufferverts[mesh.verts[face.verts[2]]][0]])      
        elif len(face.verts) == 4: # a quad must be separated into two triangles
            inds_by_material[matidx].extend([bufferverts[mesh.verts[face.verts[0]]][0],
                                             bufferverts[mesh.verts[face.verts[1]]][0],
                                             bufferverts[mesh.verts[face.verts[2]]][0]]) # first triangle
            inds_by_material[matidx].extend([bufferverts[mesh.verts[face.verts[0]]][0],
                                             bufferverts[mesh.verts[face.verts[2]]][0],
                                             bufferverts[mesh.verts[face.verts[3]]][0]]) # second triangle

        for j, vertidx in enumerate(face.verts):
            vert,vertcols,claimed_by_these_materials = bufferverts[mesh.verts[vertidx]]
            vertcols.append(col[j])
            vert.UVWs = [hsVector3(face_uvs[uvi][j][0],face_uvs[uvi][j][1],0.0) for uvi in range(len(mesh.uv_textures))]
            #add to claimed_by_these_materials
            if not matidx in claimed_by_these_materials: #I'm not sure if this is worth it.
                claimed_by_these_materials.append(matidx) # Maybe it'd be better to just let there be multiple copies of the same index
    #now our "vert of many colors" operations
    #we'll just average them for now
    #if there's a faster way to average these, please change this
    for vert in bufferverts.values():
        vert,vertcols,claimed_by_these_materials = vert
        rgbtotals = [0,0,0]
        for col in vertcols:
            rgbtotals[0]+=col[0] #r
            rgbtotals[1]+=col[1] #g
            rgbtotals[2]+=col[2] #b
        vert.color = hsColor32(round((rgbtotals[0]/float(len(vertcols)))*255.0),
                               round((rgbtotals[1]/float(len(vertcols)))*255.0),
                               round((rgbtotals[2]/float(len(vertcols)))*255.0),
                               255).color
    for mati,mat in enumerate(mesh.materials):
        print("Material %s owns %i inds."%(mat.name,len(inds_by_material[mati])))
    return bufferverts,inds_by_material

def GetPlasmaVertsAndIndsByMaterial(bufferverts, inds_by_material, material_index):
    pointerinds = inds_by_material[material_index]
    verts = []
    for vert in bufferverts.values(): #we don't need the blvert keying here
        if material_index in vert[2]: #vert[2] is claimed_by_these_materials
            verts.append(vert[0]) #the plasma vertex
    inds = []
    for ind in pointerinds:
        inds.append(verts.index(ind))
    return verts, inds

def CreateDrawableSpans(agename,scenenode,renderlevel,criteria):
    spanlabel = "Spans"
    if renderlevel > 0: #it's a blend
        spanlabel = "BlendSpans"
    one="%08x" % renderlevel
    two="%x" % criteria
    name = "%s_District_%s_%08x_%x%s"%(agename, scenenode.key.name, renderlevel, criteria, spanlabel)
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
    def __init__(self):
        self.dspans_list = []

    def AddDrawableSpans(self, dspans):
        self.dspans_list.append([dspans,[]]) #dspans and buffergroup list
        return len(self.dspans_list)-1
    
    def FindOrCreateBufferGroup(self, dspansind, UVCount,num_vertexs):
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
        print(self.dspans_list)
        # and return new index in list
        return bufferGroupInd

    def FinallizeDSpans(self,dspansind, quickymat):
        dspans,buffergroupinfos = self.dspans_list[dspansind]
        dspans.addMaterial(quickymat.key)
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
            
    def AddBlenderMeshToDSpans(self, dspansind, mesh):
        dspans,buffergroupinfos = self.dspans_list[dspansind]
        bufferverts,inds_by_material = DigestBlMesh(mesh)
        icicle_inds = []
    
        for matindex in inds_by_material:
            print("Adding geometry associated with %s"%mesh.materials[matindex].name)
            verts, inds = GetPlasmaVertsAndIndsByMaterial(bufferverts, inds_by_material, matindex)
            print("  Verts: %i"%len(verts))
            print("  UVW layers: %i"%len(mesh.uv_textures))
            buffergroup_index = self.FindOrCreateBufferGroup(dspansind,len(mesh.uv_textures),len(verts))
            print("  Buffer Group Index: %i"%buffergroup_index)
            bg = dspans.bufferGroups[buffergroup_index]
            
            vert_offset = len(buffergroupinfos[buffergroup_index].verts_to_be_written)
            inds_offset = len(buffergroupinfos[buffergroup_index].inds_to_be_written)
            buffergroupinfos[buffergroup_index].verts_to_be_written.extend(verts)
            buffergroupinfos[buffergroup_index].inds_to_be_written.extend([i+vert_offset for i in inds])
            ice = plIcicle()
            ice.groupIdx = buffergroup_index
            ice.VLength = len(verts)
            ice.VStartIdx = vert_offset
            ice.ILength = len(inds)
            ice.IStartIdx = inds_offset
            ice.materialIdx = 0 #point to our dummy material for now.
            dspans.addIcicle(ice)
            icicle_inds.append(len(dspans.spans)-1)
            
        di_ind_obj = plDISpanIndex()
        di_ind_obj.indices = icicle_inds
        dspans.addDIIndex(di_ind_obj)
        return dspans,(len(dspans.DIIndices)-1)

        
