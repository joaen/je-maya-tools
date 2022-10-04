import math
import maya.api.OpenMaya as om
import pymel.core as pm

'''
Author: Joar Engberg 2022

Description:
Takes two transforms and calculates how the rotate transform rotates around the pivot transform
based on the input rotation values and then returns a MMatrix.

'''

def rotate_around(rotate_transform, pivot_transform, degree_x=0, degree_y=0, degree_z=0):

    radian_x = math.radians(degree_x)
    radian_y = math.radians(degree_y)
    radian_z = math.radians(degree_z)

    rx_a = [1, 0, 0, 0]
    rx_b = [0, math.cos(radian_x), (-math.sin(radian_x)), 0]
    rx_c = [0, math.sin(radian_x), math.cos(radian_x), 0]
    rx_d = [0, 0, 0, 1]

    ry_a = [math.cos(radian_y), 0, math.sin(radian_y), 0]
    ry_b = [0, 1, 0, 0]
    ry_c = [(-math.sin(radian_y)), 0, math.cos(radian_y), 0]
    ry_d = [0, 0, 0, 1]

    rz_a = [math.cos(radian_z), (-math.sin(radian_z)), 0, 0]
    rz_b = [math.sin(radian_z), math.cos(radian_z), 0, 0]
    rz_c = [0, 0, 1, 0]
    rz_d = [0, 0, 0, 1]

    rotate_matrix = om.MMatrix(pm.xform(rotate_transform, query=True, matrix=True))
    pivot_matrix = om.MMatrix(pm.xform(pivot_transform, query=True, matrix=True))
    
    rot_x = om.MMatrix([rx_a, rx_b, rx_c, rx_d])
    rot_y = om.MMatrix([ry_a, ry_b, ry_c, ry_d])
    rot_z = om.MMatrix([rz_a, rz_b, rz_c, rz_d])

    output_matrix = om.MMatrix(rotate_matrix * pivot_matrix.inverse() * rot_x * rot_y * rot_z * pivot_matrix)

    return output_matrix

# Example code:
# matrix = rotate_around(rotate_transform="pSphere1", pivot_transform="pCube1", degree_y=45)
# new_locator = pm.spaceLocator()
# pm.xform(new_locator, matrix=matrix)