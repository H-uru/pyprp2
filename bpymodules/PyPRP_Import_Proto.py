#!BPY
"""
Name: 'PyPRP2'
Blender: 245
Group: 'Import'
Tip: 'PyPRP (version 2a)'
"""

import Blender
from PyPRP import PyPRP_Import

Blender.Window.FileSelector(PyPRP_Import.importFile, "Import .age or .prp")
