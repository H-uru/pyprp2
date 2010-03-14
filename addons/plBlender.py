# plasma.py  2010 Darryl Pogue
"Plasma Engine Environment"

import bpy,properties_data_modifier,space_info
import plasma

fullscreen = (lambda self, context: self.layout.operator("wm.window_fullscreen_toggle", icon='FULLSCREEN_ENTER', text=""))



##class newmod(properties_data_modifier.DATA_PT_modifiers):
##    def COLLISION2(self, layout, ob, md, wide_ui):
 ##       layout.label(text="See COLLL.")
            
def register():
    bpy.types.unregister(space_info.INFO_HT_header)
    plasma.plRegister()
    ##bpy.types.unregister(properties_data_modifier.DATA_PT_modifiers)
    ##bpy.types.register(newmod)

    ##bpy.types.register(INFO_HT_header_plasma)
    ##draw = header_draw 
    ##bpy.types.INFO_HT_header_plasma.append(fullscreen)

def unregister():
    bpy.types.unregister(INFO_MT_plasma)
