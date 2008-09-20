from Blender import *
from PyPlasma import *
import Blender
import logging

class blDrawableSpans:
    def __init__(self):
        pass
    
    def importObj(self, obj, rm, data, idx):
        logging.info("[plDrawableSpans::%s]" % (obj.key.name))
        
        if data is None:
            data = Blender.Mesh.New(obj.key.name)
        
        if (len(data.getColorLayerNames()) < 1) or not('Col' in data.getColorLayerNames()):
            data.addColorLayer('Col')
        
        data.activeColorLayer = 'Col'
        di = obj.DIIndices[idx]
        
        for ind in di.indices:
            icicle = obj.spans[ind]
            
            bufferGroup = obj.bufferGroups[icicle.groupIdx]
            if (len(data.getUVLayerNames()) < bufferGroup.numUVs):
                for uvl in range(len(data.getUVLayerNames()), bufferGroup.numUVs):
                    data.addUVLayer("UVLayer" + str(uvl))
            
            verts = obj.getVerts(icicle)
            indices = obj.getIndices(icicle)
            baseIndex = ((data.verts[-1].index+1) if ((len(data.verts)) > 0) else 0)
            
            i = 0
            logging.debug("\tImporting %i vertices." % (len(verts)))
            data.verts.extend([Mathutils.Vector(v.pos.X,v.pos.Y,v.pos.Z) for v in verts])
            for v in verts:
                vert = data.verts[i]
                if vert.index != i:
                    logging.debug("\tIndex should be %i. Is really %i." % (i + baseIndex, vert.index))
                vert.no = Mathutils.Vector(v.normal.X,v.normal.Y,v.normal.Z)
                i += 1
            
            faceIndices = data.faces.extend([[indices[(j*3)+c] + baseIndex for c in range(3)] for j in range(len(indices) / 3)], indexList=True)
            j = 0
            for faceIdx in faceIndices:
                if faceIdx is None:
                    continue
                face = data.faces[faceIdx]
                for c in range(3):
                    v = verts[indices[j+c]]
                    col = hsColor32(v.color)
                    face.col[c].r = col.red
                    face.col[c].g = col.green
                    face.col[c].b = col.blue
                    face.col[c].a = col.alpha
                    for uvl in range(bufferGroup.numUVs):
                        data.activeUVLayer = data.getUVLayerNames()[uvl]
                        face.uv[c].x = v.UVWs[uvl].X
                        face.uv[c].y = v.UVWs[uvl].Y
                j += 3
        
        return data
