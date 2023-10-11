'''
Author: Joar Engberg 2023

Description:
Rotates the rotate transform around the pivot transform using vectors.

'''

import maya.api.OpenMaya as om
import pymel.core as pm
import math


def rotate_around_pivot(x, y, z, rotate_transform, pivot_transform):
    # Move object to pivot origin and store direction and position vector
    pivot_vec = om.MVector(pm.xform(pivot_transform, query=True, worldSpace=True, translation=True))
    transform_vec = om.MVector(pm.xform(rotate_transform, worldSpace=True, query=True, translation=True))
    difference = (transform_vec - pivot_vec)
    direction = difference.normal()
    pm.xform(rotate_transform, worldSpace=True, translation=difference)
    
    # Rotate transform
    current_rotation = pm.xform(rotate_transform, query=True, worldSpace=True, rotation=True)
    pm.xform(rotate_transform, worldSpace=True, rotation=[current_rotation[0] + x, current_rotation[1] + y, current_rotation[2] + z])

    # Create quaternion and transform the direction vector
    quaternion = om.MEulerRotation(math.radians(x), math.radians(y), math.radians(z)).asQuaternion()
    new_direction = direction.rotateBy(quaternion)

    # Calculate new position
    new_pos = pivot_vec + new_direction * difference.length()
    
    # Set new position
    pm.xform(rotate_transform, translation=new_pos)

# Example code:
# rotate_around_pivot(0, 0, 30, "earth", "sun")