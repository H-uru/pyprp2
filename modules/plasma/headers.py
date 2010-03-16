import bpy,space_info,plasma
from bpy.props import *
from plasma import exporter


class INFO_MT_plasma(bpy.types.Menu):
    bl_idname = "INFO_MT_plasma"
    bl_label = "Plasma"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'EXEC_AREA'
        layout.operator("export.plasmaexportprp", text="Export Prp")
        layout.operator("wm.exit_blender", text="Quit", icon='QUIT')


class INFO_HT_header_plasma(space_info.INFO_HT_header):
    def draw(self, context):
        layout = self.layout

        window = context.window
        scene = context.scene

        row = layout.row(align=True)
        row.template_header()

        if context.area.show_menus:
            sub = row.row(align=True)
            sub.menu("INFO_MT_file")
            sub.menu("INFO_MT_add")
            sub.menu("INFO_MT_plasma")
            sub.menu("INFO_MT_help")

        if window.screen.fullscreen:
            layout.operator("screen.back_to_previous", icon='SCREEN_BACK', text="Back to Previous")
            layout.separator()
        else:
            layout.template_ID(context.window, "screen", new="screen.new", unlink="screen.delete")

        layout.template_ID(context.screen, "scene", new="scene.new", unlink="scene.delete")

        layout.separator()

        layout.template_operator_search()
        layout.template_running_jobs()

        layout.label(text=scene.statistics())

        layout.operator("wm.window_fullscreen_toggle", icon='FULLSCREEN_ENTER', text="")

def register():
    bpy.types.register(INFO_MT_plasma)
    bpy.types.register(INFO_HT_header_plasma)
    bpy.types.register(exporter.PlasmaExportPrp)
    bpy.types.register(exporter.PlasmaExportResourcePage)

    
def unregister():
    bpy.types.unregister(INFO_MT_plasma)
    bpy.types.unregister(INFO_HT_header_plasma)
    bpy.types.unregister(exporter.PlasmaExportPrp)
    bpy.types.unregister(exporter.PlasmaExportResourcePage)
