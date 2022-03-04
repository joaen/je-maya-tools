import maya.cmds as cmds
import maya.api.OpenMaya as om

def look(looker, target):
    looker_transform = looker
    target_transform = target

    looker_vec_position = cmds.xform(looker_transform, query=True, worldSpace=True, translation=True)
    target_position = cmds.xform(target_transform, query=True, worldSpace=True, translation=True)

    looker_vec = om.MVector(looker_vec_position)
    target_vec = om.MVector(target_position)
    world_up_vec = om.MVector(0,1,0)

    # Look at direction / forward direction
    z_vec = om.MVector(target_vec - looker_vec).normalize()

    # Side direction
    x_vec = om.MVector(world_up_vec ^ z_vec).normalize()

    # Calculate local up direction
    y_vec = om.MVector(z_vec ^ x_vec).normalize()

    # Compose the rotation matrix using the directions and the position of the looker object
    x = [x_vec.x, x_vec.y, x_vec.z, 0]
    y = [y_vec.x, y_vec.y, y_vec.z, 0]
    z = [z_vec.x, z_vec.y, z_vec.z, 0]
    o = [looker_vec.x, looker_vec.y, looker_vec.z, 1]
    matrix_list = [x, y, z, o]

    look_at_matrix = om.MMatrix(matrix_list)
    
    # Rotate the looker object using the rotation matrix
    cmds.xform(looker_transform, matrix=look_at_matrix)