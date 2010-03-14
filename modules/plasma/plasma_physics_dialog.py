from plasma_namespace import *

class PHYSICS_PT_plasma(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "physics"
    bl_label = "plPhysical"
    #I hope recreating this type isn't too much of a hit.  If there's a way to get context passed to the creator it could test for if it's there.
    bpy.types.Object.PointerProperty(attr="plasma_settings", type=PlasmaSettings, name="Plasma Settings", description="Plasma Engine Object Settings")

    PlasmaSettings.FloatProperty(attr="plPhysicsMass",name="Mass",default=0.0,soft_min=0,soft_max=1000)
    PlasmaSettings.FloatProperty(attr="plPhysicsFriction",name="Friction",default=0.0,soft_min=0,soft_max=1000)
    PlasmaSettings.FloatProperty(attr="plPhysicsRestitution",name="Restitution",default=0.0,soft_min=0,soft_max=1000)
    PlasmaSettings.EnumProperty(attr="plPhysicsBounds",
                              items=(
                                  ("1", "Box", ""),
                                  ("2", "Sphere", ""),
                                  ("3", "Hull", ""),
                                  ("4", "Proxy", ""),
                                  ("5", "Explicit", ""),
                                  ("6", "Cylinder", "")
                              ),
                              name="Bounds Type",
                              description="Bounds Type",
                              default="3")
    PlasmaSettings.StringProperty(attr="plPhysicsSubWorld")
    PlasmaSettings.StringProperty(attr="plPhysicsSndGroup")

    def draw(self,context):
        layout = self.layout
        view = context.object
        pl = view.plasma_settings
        layout.prop(pl, "plPhysicsMass")
        layout.prop(pl, "plPhysicsFriction")
        layout.prop(pl, "plPhysicsRestitution")
        layout.label(text="SubWorld:")
        layout.prop(pl, "plPhysicsSubWorld")
        layout.label(text="Sound Group:")
        layout.prop(pl, "plPhysicsSndGroup")
        layout.label(text="Bounds Type:")
        layout.prop(pl, "plPhysicsBounds", text="")
        
    def export(self,  blobject, plphysical):
        plphysical.mass = blobject.plasma_settings.plPhysicsMass
        plphysical.friction = blobject.plasma_settings.plPhysicsFriction
        plphysical.restitution = blobject.plasma_settings.plPhysicsRestitution
        #blobject.plPhysicsSubWorld
        plphysical.boundsType = int(blobject.plasma_settings.plPhysicsBounds)

def register():
    bpy.types.register(PHYSICS_PT_plasma)

    
def unregister():
    bpy.types.unregister(PHYSICS_PT_plasma)
