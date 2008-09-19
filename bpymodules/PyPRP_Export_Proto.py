#!BPY
"""
Name: 'PyPRP2'
Blender: 245
Group: 'Export'
Tip: 'PyPRP (version 2a)'
"""

import Blender
from PyPRP import PyPRP_Export

Blender.Window.FileSelector (PyPRP_Export.ExportMain, "Export Whole Age") # not _really_ a whole age right now. hehehe
