import bpy
from PyHSPlasma import *

class GeometryManager:
    def __init__(self):
        self.dspans = []
        

def DigestBlMesh(mesh): #Let's hope for no indigestion.
    vertex_color = mesh.vertex_colors.get("Col")
    vertex_alpha = mesh.vertex_colors.get("Alpha")
    
    inds_by_material = {}
    #create empty arrays for the face inds (pointers)
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
        v.pos.X = vert.co[0]
        v.pos.Y = vert.co[1]
        v.pos.Z = vert.co[2]
        #normal
        v.normal.X = vert.normal[0]
        v.normal.Y = vert.normal[1]
        v.normal.Z = vert.normal[2]                
        #add the stuff to the dict
        bufferverts[vert] = v,vertcols,claimed_by_these_materials
        
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
            for uvi in range(len(mesh.uv_textures)):
                vert.UVWs.append(hsVector3(face_uvs[uvi][j][0],face_uvs[uvi][j][1],0.0))
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

def AddBlenderMeshToDSpans(dspans, mesh):
    bufferverts,inds_by_material = DigestBlMesh(mesh)
    for matindex in inds_by_material:
        print("Adding geometry associated with %s"%mesh.materials[matindex].name)
        verts, inds = GetPlasmaVertsAndIndsByMaterial(bufferverts, inds_by_material, matindex)
        

    
