import bpy

def active_node_mat(mat):
    if mat:
        mat_node = mat.active_node_material
        if mat_node:
            return mat_node
        else:
            return mat

    return None

def context_tex_datablock(context):
    idblock = active_node_mat(context.material)
    if idblock:
        return idblock

    idblock = context.lamp
    if idblock:
        return idblock

    idblock = context.world
    if idblock:
        return idblock

    idblock = context.brush
    return idblock

class MATERIAL_PT_plasma(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    bl_label = "hsGMaterial"
    def draw(self, context):
        layout = self.layout

        mat = context.material
        ob = context.object
        slot = context.material_slot
        space = context.space_data
        idblock = context_tex_datablock(context)

        layout.label(text="Layers:")
        row = layout.row()

        row.template_list(idblock, "texture_slots", idblock, "active_texture_index", rows=2)

        col = row.column(align=True)
        col.operator("texture.slot_move", text="", icon='TRIA_UP').type = 'UP'
        col.operator("texture.slot_move", text="", icon='TRIA_DOWN').type = 'DOWN'
        
        layout.template_ID(idblock, "active_texture", new="texture.new")


def register():
    bpy.types.register(MATERIAL_PT_plasma)

    
def unregister():
    bpy.types.unregister(MATERIAL_PT_plasma)

