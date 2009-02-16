from Blender import *
from PyPlasma import *
import Blender
import logging

class blBase:
    def __init__(self):
       self.fKey = None
       self.fHasBeenRead = False

#class ptLog:
#    def __init__(self,handle,filename,mode="w"):
#        self.file=file(filename,mode)
#        self.handle=handle
#
#
#    def write(self,x):
#        self.handle.write(x)
#        self.file.write(x)
#
#
#    def flush():
#        self.handle.flush()
#        self.file.flush()
#
#
#    def close(self):
#        self.file.close()
