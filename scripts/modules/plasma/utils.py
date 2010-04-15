#    Copyright (C) 2010  Guild of Writers PyPRP2 Project Team
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

from PyHSPlasma import *

def transform_vector3_by_blmat(vector,m):
    x = m[0][0]*vector[0] + m[1][0]*vector[1] + m[2][0]*vector[2] + m[3][0]
    y = m[0][1]*vector[0] + m[1][1]*vector[1] + m[2][1]*vector[2] + m[3][1]
    z = m[0][2]*vector[0] + m[1][2]*vector[1] + m[2][2]*vector[2] + m[3][2]
    return [x,y,z]

def transform_vector3_by_plmat(vector,m):
    x = m[0, 0]*vector[0] + m[0, 1]*vector[1] + m[0, 2]*vector[2] + m[0, 3]
    y = m[1, 0]*vector[0] + m[1, 1]*vector[1] + m[1, 2]*vector[2] + m[1, 3]
    z = m[2, 0]*vector[0] + m[2, 1]*vector[1] + m[2, 2]*vector[2] + m[2, 3]
    return [x,y,z]

def blMatrix44_2_hsMatrix44(blmat):
    hsmat = hsMatrix44()
    for i in range(4):
        for j in range(4):
            hsmat[i,j] = blmat[j][i]
    return hsmat
