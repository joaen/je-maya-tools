'''
Name: calculate_pole_vector
Description: Caluculate the pole vector position using three input joints (Eg. Shoulder, elbow and wrist)
 
Author: Joar Engberg 2022
Installation:
Add calculate_pole_vector.py to your Maya scripts folder (Username\Documents\maya\scripts).

To calculate the pole position and create a locator at that position you can select three joints in Maya (in top-down order) and run this command or add it to a shelf button:

import calculate_pole_vector
calculate_pole_vector.create_loc(offset=2)

If you just want query the correct pole vector position you can run this commands and use your preffered transforms as input:

import calculate_pole_vector
calculate_pole_vector.get_position("pSphere1", "pSphere2", "pSphere1", offset=2)

'''

import maya.cmds as cmds
import maya.api.OpenMaya as om


def get_position(start_joint, mid_joint, end_joint, offset):
    # Get joint poistions as vectors
    joint1_pos = om.MVector(cmds.xform(start_joint, query=True, worldSpace=True, translation=True))
    joint2_pos = om.MVector(cmds.xform(mid_joint, query=True, worldSpace=True, translation=True))
    joint3_pos = om.MVector(cmds.xform(end_joint, query=True, worldSpace=True, translation=True))

    # Calculate the mid point between joint1 and joint3
    mid_point_pos = joint1_pos + (joint3_pos - joint1_pos).normal() * ((joint3_pos - joint1_pos).length() * 0.5)

    # Get the pole vector position by aiming from the mid point towards joint2 position. Scale the vector using the offset float.
    pole_vec = mid_point_pos + (joint2_pos - mid_point_pos).normal() * ((joint2_pos - mid_point_pos).length() * offset)
    
    print("Pole position: "+str(pole_vec))
    return pole_vec

def create_loc(offset=2):
    joint1 = cmds.ls(selection=True)[0]
    joint2 = cmds.ls(selection=True)[1]
    joint3 = cmds.ls(selection=True)[2]
    pole_vector_pos = get_position(joint1, joint2, joint3, offset)

    loc = cmds.spaceLocator()
    cmds.move(pole_vector_pos[0], pole_vector_pos[1], pole_vector_pos[2], loc, absolute=True, worldSpace=True)


