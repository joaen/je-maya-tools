'''
Name: calculate_pole_vector
Description: Caluculate the pole vector position using three input joints (Eg. Shoulder, elbow and wrist)
 
Author: Joar Engberg 2022
Installation:
Add calculate_pole_vector.py to your Maya scripts folder (Username\Documents\maya\scripts).

To calculate the pole position and create a locator at that position you can select three joints in Maya (in top-down order) and run this command or add it to a shelf button:

from calculate_pole_vector import create_loc
create_loc(offset="2")

'''

import pymel.core as pm

def get_position(start_joint, mid_joint, end_joint, offset):
    # Create pynodes
    joint1_node = pm.PyNode(start_joint)
    joint2_node = pm.PyNode(mid_joint)
    joint3_node = pm.PyNode(end_joint)

    # Get joint poistions
    joint1_pos = joint1_node.getTranslation(space="world")
    joint2_pos = joint2_node.getTranslation(space="world")
    joint3_pos = joint3_node.getTranslation(space="world")
    
    # Calculate the mid point between joint1 and joint3
    mid_point_pos = joint1_pos + (joint3_pos - joint1_pos).normal() * ((joint3_pos - joint1_pos).length() * 0.5)

    # get the pole vector position using the mid point and scaling the using the offset float
    pole_vec = mid_point_pos + (joint2_pos - mid_point_pos).normal() * ((joint2_pos - mid_point_pos).length() * offset)
    print("Pole position: "+str(pole_vec))
    
    return pole_vec

def create_loc(offset=2):
    joint1 = pm.selected()[0]
    joint2 = pm.selected()[1]
    joint3 = pm.selected()[2]
    pole_vector_pos = get_position(joint1, joint2, joint3, offset)
    pm.spaceLocator().setTranslation(pole_vector_pos, space="world")

