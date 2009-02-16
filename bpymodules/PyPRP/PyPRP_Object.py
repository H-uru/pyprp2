from PyPlasma import *
from PyPRP_Geometry import *
from PyPRP_Light import *
from PyPRP_Physics import *
import Blender
import logging

class blSceneObject:
    def __init__(self):
        pass
    
    def importObj(self, obj, rm, scn):
        logging.info("[plSceneObject::%s]" % (obj.key.name))
        
        data = None
        layers = [1]
        
        if obj.draw and obj.draw.object:
            logging.debug("\tWe have a DrawInterface!")
            drawiface = plDrawInterface.Convert(obj.draw.object)
            di = blDrawInterface()
            data = di.importObj(drawiface, rm)
        
        if obj.sim and obj.sim.object:
            logging.debug("\tWe have a SimulationInterface!")
            simiface = plSimulationInterface.Convert(obj.sim.object)
            si = blSimulationInterface()
            if data != None:
                si.importObj(simiface, rm, scn)
            else:
                data = si.importObj(simiface, rm)
                layers = [2]
        
        if data is None:
            data = 'Empty'
        
        #Handle interfaces
        
        for mod in obj.modifiers:
            if mod.type == plFactory.kSpawnModifier: #SpawnModifier
                data = 'Empty'
                layers = [2]
            elif mod.type == plFactory.kPostEffectMod: #PostEffectModifier
                data = Blender.Camera.New('ortho', obj.key.name)
                layers = [2]
            elif mod.type == plFactory.kCameraModifier: #CameraModifier
                data = Blender.Camera.New('persp', obj.key.name)
                layers = [2]
        
        for iface in obj.interfaces:
            if iface.type is plFactory.kDirectionalLightInfo:
                data = Blender.Lamp.New('Sun', iface.name)
                layers = [3]
            elif iface.type is plFactory.kOmniLightInfo:
                oli = plOmniLightInfo.Convert(iface.object)
                bli = blOmniLightInfo()
                data = bli.importObj(oli, rm)
                layers = [3]
            elif iface.type is plFactory.kSpotLightInfo:
                data = Blender.Lamp.New('Spot', iface.name)
                layers = [3]
            elif iface.type is plFactory.kLimitedDirLightInfo:
                data = Blender.Lamp.New('Area', iface.name)
                layers = [3]
            elif iface.type is plFactory.kOccluder:
                occ = plOccluder.Convert(iface.object)
                oci = blOccluder()
                data = oci.importObj(occ, rm)
                layers = [5]
        
        blObj = scn.objects.new(data, obj.key.name)
        
        if obj.coord and obj.coord.object:
            logging.debug("\tWe have a CoordinateInterface!")
            coordiface = plCoordinateInterface.Convert(obj.coord.object)
            ci = blCoordinateInterface()
            ci.importObj(coordiface, rm, blObj)
        
        blObj.layers = layers
        return blObj
    
    def Export(self,rm,loc,blObj):
        so = plSceneObject(blObj.name)
        so.sceneNode = rm.getSceneNode(loc).key
        if blObj.type == 'Mesh':
            DrawInterface = blDrawInterface()
            so.draw = DrawInterface.Export(rm,loc,blObj,so).key
        rm.AddObject(loc, so)
        return so

class blCoordinateInterface:
    def __init__(self):
        pass
    
    def importObj(self, obj, rm, blObj):
        logging.info("[plCoordinateInterface::%s]" % (obj.key.name))
        m = Blender.Mathutils.Matrix(obj.localToWorld.mat[0], obj.localToWorld.mat[1], obj.localToWorld.mat[2], obj.localToWorld.mat[3])
        m.transpose()
        blObj.setMatrix(m)
    
    def Export(self,rm,loc,name):
        rm.AddObject(loc,self)

class blSimulationInterface:
    def __init__(self):
        pass
    
    def importObj(self, obj, rm, scn = None):
        logging.info("[plSimulationInterface::%s]" % (obj.key.name))
        
        if obj.physical.object:
            phy = plGenericPhysical.Convert(obj.physical.object)
            blp = blPhysical()
            data = blp.importObj(phy, rm, scn != None)
            
            if scn:
                nObj = scn.objects.new(data, "Col" + obj.key.name)
                nObj.layers = [2]
                return None
            else:
                return data
        
        return "Empty"
            
    
    def Export(self,rm,loc,name):
        rm.AddObject(loc,self)

class blDrawInterface:
    def __init__(self):
        pass
    
    def importObj(self, obj, rm):
        logging.info("[plDrawInterface::%s]" % (obj.key.name))
        data = None
        for drawable in obj.drawables:
            if drawable[1] is -1:
                continue
            
            dspan = plDrawableSpans.Convert(drawable[0].object)
            span = blDrawableSpans()
            data = span.importObj(dspan, rm, data, drawable[1], obj.key.name)
        
        if data is not None:
            data.calcNormals()
        return data

    def Export(self,rm,loc,blObj,so):
        di = plDrawInterface(blObj.name)
        di.owner = so.key
        rm.AddObject(loc,di)
        return di

class blAudioInterface:
    def Export(self,rm,loc,name):
        rm.AddObject(loc,self)

class blOccluder:
    def __init__(self):
        pass
    
    def importObj(self, obj, rm):
        logging.info("[plOccluder::%s]" % (obj.key.name))
        data = Blender.Mesh.New(obj.key.name)

        for p in obj.polys:
            baseIndex = ((data.verts[-1].index+1) if ((len(data.verts)) > 0) else 0)
            data.verts.extend([Mathutils.Vector(v.X,v.Y,v.Z) for v in p.verts])
            i = 0
            for v in p.verts:
                vert = data.verts[i]
                if vert.index != i:
                    logging.debug("\tIndex should be %i. Is really %i." % (i + baseIndex, vert.index))
                vert.no = Mathutils.Vector(p.norm.X,p.norm.Y,p.norm.Z)
                i += 1
            
            if len(p.verts) is 3 or len(p.verts) is 4:
                data.faces.extend([c + baseIndex for c in range(len(p.verts))], indexList=True)
        
        return data
