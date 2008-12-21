from PyPlasma import *
from PyPRP_Geometry_Classes import *
import Blender
import logging

class blSceneObject:
    def __init__(self):
        pass
    
    def importObj(self, obj, rm, scn):
        logging.info("[plSceneObject::%s]" % (obj.key.name))
        
        data = 'Empty'
        
        if obj.draw and obj.draw.object:
            logging.debug("\tWe have a DrawInterface!")
            drawiface = plDrawInterface.Convert(obj.draw.object)
            di = blDrawInterface()
            data = di.importObj(drawiface, rm)
        if data is None:
            data = 'Empty'
        
        #Handle interfaces
        
        for mod in obj.modifiers:
            if mod.type == plFactory.kSpawnModifier: #SpawnModifier
                data = 'Empty'
        
        blObj = scn.objects.new(data, obj.key.name)
        
        if obj.coord and obj.coord.object:
            logging.debug("\tWe have a CoordinateInterface!")
            coordiface = plCoordinateInterface.Convert(obj.coord.object)
            ci = blCoordinateInterface()
            ci.importObj(coordiface, rm, blObj)
        
        if obj.sim and obj.sim.object:
            logging.debug("\tWe have a SimulationInterface!")
            simiface = plSimulationInterface.Convert(obj.sim.object)
            si = blSimulationInterface()
            si.importObj(simiface, rm, blObj)
        
        return blObj
    
    def Export(self,rm,loc,blObj):
        so = plSceneObject(blObj.name)
        so.sceneNode = rm.getSceneNode(loc).key
        if blObj.type == 'Mesh':
            DrawInterface = blDrawInterface()
            so.draw = DrawInterface.Export(rm,loc,blObj,so).key
        rm.AddObject(loc, so)
        return so

    def Import(self,rm,obj,scn):
        print "  Importing SceneObject %s" % obj.key.name

        CameraMod = False
        LightInfo = False
        SpawnMod = False

        for inter in obj.interfaces:
            #LampInfo
            if inter.type == plFactory.kDirectionalLightInfo:
                LightInfo = 'Sun'
            elif inter.type == plFactory.kOmniLightInfo:
                LightInfo = 'Lamp'
            elif inter.type == plFactory.kSpotLightInfo:
                LightInfo = 'Spot'
            elif inter.type == plFactory.kLimitedDirLightInfo:
                LightInfo = 'Area'

        for mod in obj.modifiers:
            if mod.type in [plFactory.kCameraModifier,plFactory.kCameraModifier1]: #CameraModifier
                CameraMod = True

        for mod in obj.modifiers:
            if mod.type == plFactory.kSpawnModifier: #SpawnModifier
                SpawnMod = True
        DIKey = obj.draw
        if DIKey:
            self.BlenderObject = scn.objects.new(Blender.Mesh.New(obj.key.name),obj.key.name)
        elif CameraMod:
            Cam = Blender.Camera.New('persp')
            Cam.lens = 16.0
            self.BlenderObject = scn.objects.new(Cam,obj.key.name)
        elif LightInfo:
            self.BlenderObject = scn.objects.new(Blender.Lamp.New(LightInfo),obj.key.name)
        elif SpawnMod:
            self.BlenderObject = scn.objects.new('Empty',obj.key.name) #can set some props later but for now it'll just be an empty
        else:
            self.BlenderObject = scn.objects.new('Empty',obj.key.name)
            self.BlenderObject.layers = [2]
        #second leg: Classes connected to me: "Get yer data into Blender"
        CIKey = obj.coord
        if CIKey:
            CI = CIKey.object
            if CI:
                CIobj = plCoordinateInterface.Convert(CI)
                BL_CI = blCoordinateInterface()
                BL_CI.Import(rm,self,CIobj)
        DIKey = obj.draw
        if DIKey:
            DI = DIKey.object
            if DI:
                DIobj = plDrawInterface.Convert(DI)
                BL_DI = blDrawInterface()
                BL_DI.Import(DIobj,self.BlenderObject)

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
    
    def importObj(self, obj, rm, blObj):
        logging.info("[plSimulationInterface::%s]" % (obj.key.name))
    
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
            span.ImportObject(dspan,blObj,drawable[1])
            data = span.importObj(dspan, rm, data, drawable[1])
        
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
