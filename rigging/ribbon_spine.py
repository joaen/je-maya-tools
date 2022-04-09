'''
Name: ribbon_spine
Description: Create a joint chain with a even spacing between the joints.
Select the first in the joint hierarchy and run the script to create a ribbon spine.
 
Author: Joar Engberg 2022

'''

import maya.mel as mel
import maya.cmds as cmds

def create_ribbon():
    ribbon_jnt_list = []
    dupe_jnt_list = []
    jnt_list = []
    selection = cmds.ls(selection=True)

    jnt_list.append(selection[0])
    children =  cmds.listRelatives(selection, allDescendents=True)

    for i in reversed(range(len(children))):
        jnt_list.append(children[i])

    # Create plane using the IK spline curve.
    temp_ik_handle = cmds.ikHandle(startJoint=jnt_list[0], endEffector=jnt_list[len(jnt_list) - 1], sol="ikSplineSolver", simplifyCurve=False, rootOnCurve=False, parentCurve=False)
    cmds.delete(temp_ik_handle[0], temp_ik_handle[1])
    curve = temp_ik_handle[2]
    curve_dupe = cmds.duplicate(curve)
    cmds.move(0.25, 0, 0, curve, relative=True, objectSpace=True, worldSpaceDistance=True)
    cmds.move(-0.25, 0, 0, curve_dupe, relative=True, objectSpace=True, worldSpaceDistance=True)
    
    plane = cmds.loft(curve_dupe, curve, constructionHistory=False, range=False, autoReverse=True)
    cmds.delete(curve, curve_dupe)

    # Create follicles using the hairSystem
    cmds.select(plane, replace=True)
    mel.eval("createHair 1 {} 10 0 0 1 0 5 0 2 1 1;".format(len(jnt_list)))  
    cmds.delete("hairSystem1OutputCurves", "hairSystem1", "nucleus1")

    follicle_list = cmds.listRelatives("hairSystem1Follicles", children=True)
    for i in range(len(follicle_list)):
        jnt = cmds.joint(p=(0, 0, 0))

        ribbon_jnt_list.append(jnt)

        cmds.parent(jnt, follicle_list[i])
        cmds.xform(jnt, t=(0, 0, 0))

        dupe = cmds.duplicate(jnt)[0]
        dupe_jnt_list.append(dupe)
        cmds.parent(dupe, world=True)
        cmds.parentConstraint(jnt, jnt_list[i], maintainOffset=True)

    cmds.skinCluster(dupe_jnt_list, plane)

    for i in range(len(dupe_jnt_list)):
        cmds.rename(dupe_jnt_list[i], "spine_control_jnt{}".format(i + 1))

    for i in range(len(ribbon_jnt_list)):
        cmds.rename(ribbon_jnt_list[i], "geometry_control_jnt{}".format(i + 1))


if __name__ == "__main__":
    create_ribbon()
