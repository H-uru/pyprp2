#    This file is part of PyPRP2.
#    
#    Copyright (C) 2010 PyPRP2 Project Team
#    See the file AUTHORS for more info about the team.
#    
#    PyPRP2 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    
#    PyPRP2 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with PyPRP2.  If not, see <http://www.gnu.org/licenses/>.

def getModPropName(data_id, variable):
    return '["%i:%s"]'%(data_id, variable)

#this class can be extended to set all the _RNA_UI settings
def modVariable(obj, data_id, varname, default, min=-100, max=100):
    if not obj.get("_RNA_UI"):
        obj["_RNA_UI"] = {}
    key = "%i:%s"%(data_id, varname)
    obj[key] = default
    obj["_RNA_UI"][key] = {"min":min, "max":max, "soft_min":min, "soft_max":max}
    return key

def drawCheesyEnum(layout, data, property, enumlist, text=""):
    key = eval(property)[0] #hack
    val = data[key]
    box = layout.box()
    box.prop(data, property, text=text)
    box.label(text=enumlist[val])

def getNextAvailableDataID(mods):
    allocated = []
    for mod in mods:
        allocated.append(mod.data_id)
    i = 0
    while 1:
        if not i in allocated:
            return i
        i+=1

def getDataValue(obj, mod, variable):
    return obj["%i:%s"%(mod.data_id, variable)]
