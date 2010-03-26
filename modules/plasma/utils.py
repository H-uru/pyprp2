from PyHSPlasma import *

def transform_vector3_by_blmat(vector,m):
    x = m[0][0]*vector[0] + m[1][0]*vector[1] + m[2][0]*vector[2] + m[3][0]
    y = m[0][1]*vector[0] + m[1][1]*vector[1] + m[2][1]*vector[2] + m[3][1]
    z = m[0][2]*vector[0] + m[1][2]*vector[1] + m[2][2]*vector[2] + m[3][2]
    return [x,y,z]

def transform_vector3_by_plmat(vector,m):
    x = m[0, 0]*vector[0] + m[1, 0]*vector[1] + m[2, 0]*vector[2] + m[3, 0]
    y = m[0, 1]*vector[0] + m[1, 1]*vector[1] + m[2, 1]*vector[2] + m[3, 1]
    z = m[0, 2]*vector[0] + m[1, 2]*vector[1] + m[2, 2]*vector[2] + m[3, 2]
    return [x,y,z]

def blMatrix44_2_hsMatrix44(blmat):
    hsmat = hsMatrix44()
    for i in range(4):
        for j in range(4):
            hsmat[i,j] = blmat[j][i]
    return hsmat
