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
            
            bufferGroup = obj.bufferGroups[icicle.IBufferIdx]
            if (len(data.getUVLayerNames()) < bufferGroup.numUVs):
                for uvl in range(len(data.getUVLayerNames()), bufferGroup.numUVs):
                    data.addUVLayer("UVLayer" + str(uvl))
            
            verts = obj.getVerts(icicle)
            indices = obj.getIndices(icicle)
            baseIndex = ((data.verts[-1].index+1) if ((len(data.verts)) > 0) else 0)
            
            i = baseIndex
            logging.debug("\tImporting %i vertices." % (len(verts)))
            for v in verts:
                data.verts.extend((Mathutils.Vector(v.pos.X,v.pos.Y,v.pos.Z)))
                vert = data.verts[-1]
                if vert.index != i:
                    logging.debug("\tIndex should be %i. Is really %i." % (i, vert.index))
                i += 1
                vert.no = Mathutils.Vector(v.normal.X,v.normal.Y,v.normal.Z)
            
            j = 0
            while j < len(indices):
                f = [indices[j] + baseIndex, indices[j+1] + baseIndex, indices[j+2] + baseIndex]
                data.faces.extend(f)
                
                face = data.faces[-1]
                for c in range(3):
                    v = verts[indices[j+c]]
                    col = hsColor32()
                    col.set(v.color)
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

            bufferGroup = bufGroups[ice.IBufferIdx]
            UV_count = bufferGroup.numUVs
            UVLayers = mesh.getUVLayerNames()
            LenUVLayers = len(UVLayers)
            if LenUVLayers < UV_count:
                for i in range(LenUVLayers,UV_count):
                    mesh.addUVLayer("UVLayer" + str(i))
            UVLayers = mesh.getUVLayerNames()
            plVerts = span.getVerts(ice)
            print "        Importing %i verts..." % len(plVerts)
            for v in plVerts:
                verts.append(v)
                mesh.verts.extend((Mathutils.Vector(v.pos.X,v.pos.Y,v.pos.Z)))

                vertidx = len(mesh.verts)-1
                vert = mesh.verts[vertidx]
                vert.no = Mathutils.Vector(v.normal.X,v.normal.Y,v.normal.Z)

            indices = span.getIndices(ice)
            
            j = 0
            while j < len(indices):
                plface = [(indices[j] + s_BaseIndex),(indices[j+1] + s_BaseIndex),(indices[j+2] + s_BaseIndex)]
#                print plface
                mesh.faces.extend(plface)

                blface = mesh.faces[len(mesh.faces)-1]
                for vi in range(3):
                    vert = verts[plface[vi]]
                    col = hsColor32()
                    col.set(vert.color)
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
