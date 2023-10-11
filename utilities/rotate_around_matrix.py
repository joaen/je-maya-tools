'''
Author: Joar Engberg 2023

Description:
Rotates the rotate transform around the pivot transform using matrices.

'''

import maya.api.OpenMaya as om
import pymel.core as pm
import math


def rotate_around_pivot(x, y, z, rotate_transform, pivot_transform):
    # Get matrices from transforms
    transform_matrix = om.MMatrix(pm.xform(rotate_transform, query=True, matrix=True))
    pivot_matrix = om.MMatrix(pm.xform(pivot_transform, query=True, matrix=True))

    # Create new rotation matrix and apply rotation
    rotation_matrix = om.MMatrix()
    transform_matrix = om.MTransformationMatrix(rotation_matrix)
    rotation = om.MVector(math.radians(x),  math.radians(y), math.radians(z))
    transform_matrix.setRotation(om.MEulerRotation(rotation))

    # Compose new matrix
    rotated_matrix = pivot_matrix.inverse() * transform_matrix.asMatrix() * (pivot_matrix * transform_matrix)
    
    # Apply new matrix
    pm.xform(rotate_transform, matrix=rotated_matrix)

# Example code:
# rotate_around_pivot(30, 0, 0, "earth", "sun")