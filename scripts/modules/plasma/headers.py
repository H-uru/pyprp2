#    Copyright (C) 2010 PyPRP2 Project Team
#    See the file AUTHORS for more info about the team
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#    Please see the file LICENSE for the full license.

import bpy,space_info,plasma
from bpy.props import *
from plasma import exporter


class INFO_MT_plasma(bpy.types.Menu):
    bl_idname = "INFO_MT_plasma"
    bl_label = "Plasma"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'EXEC_AREA'
        layout.operator_menu_enum("export.plasmaexport","type", text="Export")
        #keeping this from being just export for if there's some tool we want in this menu


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
    bpy.types.register(exporter.PlasmaExport)
    bpy.types.register(exporter.PlasmaExportResourcePage)
    bpy.types.register(exporter.PlasmaExportAge)
    
def unregister():
    bpy.types.unregister(INFO_MT_plasma)
    bpy.types.unregister(INFO_HT_header_plasma)
    bpy.types.unregister(exporter.PlasmaExport)
    bpy.types.unregister(exporter.PlasmaExportResourcePage)
    bpy.types.unregister(exporter.PlasmaExportAge)

