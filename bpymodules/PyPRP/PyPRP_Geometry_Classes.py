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
            
            i = baseIndex
            logging.debug("\tImporting %i vertices." % (len(verts)))
            data.verts.extend([Mathutils.Vector(v.pos.X,v.pos.Y,v.pos.Z) for v in verts])
            for v in verts:
                vert = data.verts[i]
                if vert.index != i:
                    logging.debug("\tIndex should be %i. Is really %i." % (i, vert.index))
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
    
    def ImportObject(self,span,blenderobject,key):
        print "      Importing mesh with key %i from %s" % (key,span.key.name)
        mesh = blenderobject.getData(False,True)
        mesh.addColorLayer("Color")
        mesh.activeColorLayer = "Color"
        di = span.DIIndices[key] #plDISpanIndex
        
        s_BaseIndex = 0
        verts = []
        bufGroups = span.bufferGroups

        for idx in di.indices:
            ice = span.spans[idx] #plIcicle

            bufferGroup = bufGroups[ice.groupIdx]
            UV_count = bufferGroup.numUVs
            UVLayers = mesh.getUVLayerNames()
            LenUVLayers = len(UVLayers)
            if LenUVLayers < UV_count:
                for i in range(LenUVLayers,UV_count):
                    mesh.addUVLayer("UVLayer" + str(i))
            UVLayers = mesh.getUVLayerNames()
            plVerts = span.getVerts(ice)
            print "        Importing %i verts..." % len(plVerts)

            vertidx = len(mesh.verts)
            verts.extend(plVerts)
            mesh.verts.extend([Mathutils.Vector(v.pos.X,v.pos.Y,v.pos.Z) for v in plVerts])
            for v in plVerts:
                vert = mesh.verts[vertidx]
                vert.no = Mathutils.Vector(v.normal.X,v.normal.Y,v.normal.Z)
                vertidx += 1

            indices = span.getIndices(ice)
            
            faceIndices = mesh.faces.extend([[indices[(j*3)+c] + s_BaseIndex for c in range(3)] for j in range(len(indices) / 3)], indexList=True)
            j = 0
            for faceIdx in faceIndices:
                if faceIdx is None:
                    continue
                blface = mesh.faces[faceidx]
                for vi in range(3):
                    vert = verts[indices[j+vi]]
                    col = hsColor32(vert.color)
                    blface.col[vi].r = col.red
                    blface.col[vi].g = col.green
                    blface.col[vi].b = col.blue
                    blface.col[vi].a = col.alpha
                    for uvidx in range(UV_count):
                        mesh.activeUVLayer = UVLayers[uvidx] #UVLayerName
                        blface.uv[vi].x = vert.UVWs[uvidx].X
                        blface.uv[vi].y = vert.UVWs[uvidx].Y #used to be 1-vert.UVWs[uvidx].Y not sure if this is important
                j += 3
            s_BaseIndex += ice.VLength
        
        mesh.calcNormals()
