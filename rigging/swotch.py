import maya.cmds as cmds
import maya.api.OpenMaya as om


def switch():
    # Attritbute
    ikfk_attr_name = "CTRL_L__WristPinner.IKFK"
    ikfk_attr_value = cmds.getAttr(ikfk_attr_name)

    # FK

    fk_ctrl_start = "CTRL_FK_L__Shoulder"
    fk_ctrl_mid = "CTRL_FK_L__Elbow"
    fk_ctrl_end = "CTRL_FK_L__Wrist"
    
    ik_target_start = "rig_L__Shoulder_IK"
    ik_target_mid = "rig_L__Elbow_IK"
    ik_target_end = "rig_L__Wrist_IK"

    # IK 
    ik_ctrl = "CTRL_L__Hand"
    ik_pv_ctrl = "CTRL_L__ElbowPole"

    fk_target_start = "rig_L__Shoulder_FK"
    fk_target_mid = "rig_L__Elbow_FK"
    fk_target_end = "rig_L__Wrist_FK"

    if ikfk_attr_value == 1:
        # Set attribute
        cmds.setAttr(ikfk_attr_name, 0)

        # IK controller
        pos = om.MVector(cmds.xform(fk_target_end, query=True, translation=True, worldSpace=True))
        mat = om.MMatrix(cmds.xform(fk_target_end, query=True, matrix=True, worldSpace=True))
        
        side_vector = om.MVector(mat[0], mat[1], mat[2])
        up_vector = om.MVector(mat[4], mat[5], mat[6])
        fwd_vector = om.MVector(mat[8], mat[9], mat[10])

        x = [side_vector.x, side_vector.y, side_vector.z, 0]
        y = [up_vector.x, up_vector.y, up_vector.z, 0]
        z = [fwd_vector.x, fwd_vector.y, fwd_vector.z, 0]
        o = [pos.x, pos.y, pos.z, 1]

        matrix_list = [x, y, z, o]
        target_matrix = om.MMatrix(matrix_list)
        cmds.xform(ik_ctrl, matrix=target_matrix, worldSpace=True)

        # Pole vector
        cmds.matchTransform(ik_pv_ctrl, fk_target_mid, position=True)

    elif ikfk_attr_value == 0:
        # Set attribute
        cmds.setAttr(ikfk_attr_name, 1)

        cmds.matchTransform(fk_ctrl_start, ik_target_start, rotation=True)
        cmds.matchTransform(fk_ctrl_mid, ik_target_mid, rotation=True)
        cmds.matchTransform(fk_ctrl_end, ik_target_end, rotation=True)
    
switch()