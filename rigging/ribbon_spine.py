import maya.mel as mel
import maya.cmds as cmds

def create_ribbon():
    selection = cmds.ls(selection=True)
    point_list = []
    joints = []
    dupes = []

    # Add joint positions to list
    for j in selection:
        joint_pos = cmds.xform(j, query=True, translation=True, worldSpace=True)
        point_list.append(joint_pos)

    # Create plane
    temp_ik_handle = cmds.ikHandle(startJoint=selection[0], endEffector=selection[len(selection) - 1], sol="ikSplineSolver", simplifyCurve=False, rootOnCurve=False, parentCurve=False)
    cmds.delete(temp_ik_handle[0], temp_ik_handle[1])
    curve = temp_ik_handle[2]
    curve_dupe = cmds.duplicate(curve)
    cmds.move(0.5, 0, 0, curve, relative=True, objectSpace=True, worldSpaceDistance=True)
    cmds.move(-0.5, 0, 0, curve_dupe, relative=True, objectSpace=True, worldSpaceDistance=True)
    
    plane = cmds.loft(curve_dupe, curve, constructionHistory=False, range=False, autoReverse=True)
    cmds.delete(curve, curve_dupe)

    # Create follicles
    cmds.select(plane, replace=True)
    mel.eval("createHair 1 {} 10 0 0 1 0 5 0 2 1 1;".format(len(selection)))  
    cmds.delete("hairSystem1OutputCurves", "hairSystem1", "nucleus1")

    # Create joints
    follicle_list = cmds.listRelatives("hairSystem1Follicles", children=True)

    for i in range(len(follicle_list)):
        jnt = cmds.joint(p=(0, 0, 0))

        joints.append(jnt)

        cmds.parent(jnt, follicle_list[i])
        cmds.xform(jnt, t=(0, 0, 0) )

        dupe = cmds.duplicate(jnt)[0]
        dupes.append(dupe)
        cmds.parent(dupe, world=True)
        cmds.parentConstraint(jnt, selection[i], maintainOffset=True)

    # Skin joints to plane
    cmds.skinCluster(dupes, plane)

    for i in dupes:
        cmds.rename(i, "spine_control_jnt#")

    for i in joints:
        cmds.rename(i, "geometry_control_jnt#")


create_ribbon()