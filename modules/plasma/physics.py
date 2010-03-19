import bpy

class Physical(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "physics"
    bl_label = "Plasma Physical"
    def __init__(self, thing1):
        bpy.types.Panel.__init__(self)
        #I hope recreating this type isn't too much of a hit.  If there's a way to get context passed to the creator it could test for if it's there.
        bpy.types.Object.PointerProperty(attr="plasma_settings", type=bpy.types.PlasmaSettings, name="Plasma Settings", description="Plasma Engine Object Settings")

        bpy.types.PlasmaSettings.FloatProperty(attr="physicsmass",name="Mass",default=0.0,soft_min=0,soft_max=1000)
        bpy.types.PlasmaSettings.FloatProperty(attr="physicsfriction",name="Friction",default=0.0,soft_min=0,soft_max=1000)
        bpy.types.PlasmaSettings.FloatProperty(attr="physicsrestitution",name="Restitution",default=0.0,soft_min=0,soft_max=1000)
        bpy.types.PlasmaSettings.EnumProperty(attr="physicsbounds",
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
        bpy.types.PlasmaSettings.StringProperty(attr="physicssubworld")
        bpy.types.PlasmaSettings.StringProperty(attr="physicssndgroup")

    def draw(self,context):
        layout = self.layout
        view = context.object
        pl = view.plasma_settings
        layout.prop(pl, "physicsmass")
        layout.prop(pl, "physicsfriction")
        layout.prop(pl, "physicsrestitution")
        layout.label(text="SubWorld:")
        layout.prop(pl, "physicssubworld")
        layout.label(text="Sound Group:")
        layout.prop(pl, "physicssndgroup")
        layout.label(text="Bounds Type:")
        layout.prop(pl, "physicsbounds", text="")
        
    def export(self,  blobject, plphysical):
        plphysical.mass = blobject.plasma_settings.physicsmass
        plphysical.friction = blobject.plasma_settings.physicsfriction
        plphysical.restitution = blobject.plasma_settings.physicsrestitution
        #blobject.plPhysicsSubWorld
        plphysical.boundsType = int(blobject.plasma_settings.physicsbounds)

def register():
    bpy.types.register(Physical)

    
def unregister():
    bpy.types.unregister(Physical)
