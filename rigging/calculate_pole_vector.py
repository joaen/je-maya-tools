'''
Name: calculate_pole_vector
Description: Caluculate the pole vector position using three input joints (Eg. Shoulder, elbow and wrist)
 
Author: Joar Engberg 2022
Installation:
Add calculate_pole_vector.py to your Maya scripts folder (Username\Documents\maya\scripts).

To calculate the pole position and create a locator at that position you can select three joints in Maya (in top-down order) and run this command or add it to a shelf button:

import calculate_pole_vector
calculate_pole_vector.create_loc()

If you just want query the correct pole vector position you can run this commands and use your preffered transforms as input:

import calculate_pole_vector
calculate_pole_vector.get_position("pSphere1", "pSphere2", "pSphere1")

'''

import maya.cmds as cmds
from maya.api import OpenMaya


def get_position(start_joint, mid_joint, end_joint):
    # Get joint poistions as vectors
    joint1_point = OpenMaya.MVector(cmds.xform(start_joint, query=True, worldSpace=True, translation=True))
    joint2_point = OpenMaya.MVector(cmds.xform(mid_joint, query=True, worldSpace=True, translation=True))
    joint3_point = OpenMaya.MVector(cmds.xform(end_joint, query=True, worldSpace=True, translation=True))

    # Get the average distance between joints
    average_distance = ((joint3_point - joint2_point).length() + (joint1_point - joint2_point).length()) / 2

    # Create vectors pointing from joint2 towards joint3 and joint2 towards joint1. Scale the vectors using the average distance.
    start_joint_vector = joint2_point + (joint1_point - joint2_point).normal() * average_distance
    end_joint_vector = joint2_point + (joint3_point - joint2_point).normal() * average_distance

    # Create a new vector pointing between the start_joint_vector and end_joint_vector, and then scale it 50%.
    mid_point = start_joint_vector + (end_joint_vector - start_joint_vector).normal() * ((end_joint_vector - start_joint_vector).length() * 0.5)

    # Create a vector pointing from the mid point towards joint 2 and scale it using the average distance
    pole_vector = mid_point + (joint2_point - mid_point).normal() * average_distance
    return pole_vector

def create_loc():
    joint1 = cmds.ls(selection=True)[0]
    joint2 = cmds.ls(selection=True)[1]
    joint3 = cmds.ls(selection=True)[2]
    pole_vector_pos = get_position(joint1, joint2, joint3)

    loc = cmds.spaceLocator()
    cmds.move(pole_vector_pos[0], pole_vector_pos[1], pole_vector_pos[2], loc, absolute=True, worldSpace=True)


