import maya.api.OpenMaya as om
import pymel.core as pm

def pole_vector_position(start_joint, mid_joint, end_joint):
    start_node = pm.PyNode(start_joint)
    mid_node = pm.PyNode(mid_joint)
    end_node = pm.PyNode(end_joint)

    start_vec = start_node.getTranslation(World=True)
    mid_vec = mid_node.getTranslation(World=True)
    end_vec = end_node.getTranslation(World=True)

    start_end_dir = (end_vec - start_vec)


    mid_point_vec = start_vec + start_end_dir.normal() * (start_end_dir.length() * 0.5)

    mid_to_mid = (mid_vec - mid_point_vec)

    pole_vector = mid_point_vec + mid_to_mid.normal() * (mid_to_mid.length() * 2)
    print(pole_vector)
    return pole_vector


pole = pole_vector_position("locator1", "locator2", "locator3")
# print(pole_vector_position(pm.selected[0], pm.selected[1], pm.selected[2]))
pm.spaceLocator().setTranslation(pole, space="world")
# print(pole_vector_pos)