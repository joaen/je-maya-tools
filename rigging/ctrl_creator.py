import pymel.core as pm


def get_cvs(object):
    spans = str(pm.getAttr(object+".spans") - 1)
    ctrl_vertices = "{shape}.cv[0:{count}]".format(shape=object, count=spans)
    return ctrl_vertices

def create_controller():
    for transform in pm.selected():
        shape = get_sphere()
        pm.rename(shape, transform+"_CTRL")
        offset_grp = pm.group(shape)
        pm.rename(offset_grp, transform+"_CTRL_Grp")
        pm.matchTransform(offset_grp, transform)

def scale_ctrl_shape(size):
    stored_selection = pm.ls(selection=True)

    for ctrl in pm.selected():
        pm.select(get_cvs(ctrl), replace=True)
        pm.scale(size, size, size)
    
    pm.select(clear=True)
    for sel in stored_selection:
        pm.select(sel, add=True)

def rotate_ctrl_shape(degrees):
    stored_selection = pm.ls(selection=True)

    for ctrl in pm.selected():
        ctrl_pivot = pm.xform(ctrl, query=True, translation=True, worldSpace=True)
        pm.select(get_cvs(ctrl), replace=True)
        pm.rotate(degrees, relative=True, pivot=(ctrl_pivot))

    pm.select(clear=True)
    for sel in stored_selection:
        pm.select(sel, add=True)

def get_sphere():
    circles = []
    for n in range(0, 5):
        circles.append(pm.circle(normal=(0,0,0), center=(0,0,0))[0])

    circles[0].setRotation([0, 45, 0])
    circles[1].setRotation([0, -45, 0])
    circles[2].setRotation([0, -90, 0])
    circles[3].setRotation([90, 0, 0])
    
    # Combine
    shape_nodes = pm.listRelatives(circles, shapes=True)
    output_node = pm.group(empty=True)
    pm.makeIdentity(circles, apply=True, t=True, r=True, s=True)
    pm.parent(shape_nodes, output_node, shape=True, relative=True)
    pm.delete(shape_nodes, constructionHistory=True)
    pm.delete(circles)
    return output_node

def get_circle():
    return pm.circle(normal=(1, 0, 0), center=(0, 0, 0))

def get_cube():
    return pm.curve(name="shape123", d=1, p=[(-1, -1, 1), (-1, 1, 1), (1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, -1, -1), (-1, 1, -1), (-1, 1, 1), (-1, 1, -1), (1, 1, -1), (1, -1, -1), (-1, -1, -1), (1, -1, -1), (1, -1, 1), (1, 1, 1), (1, 1, -1)], k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

def get_square():
    return pm.curve(d=1, p=[(-1, 0, 1), (-1, 0, 1), (0, 0, 1), (1, 0, 1), (1, 0, 1), (1, 0, -1), (-1, 0, -1), (-1, 0, 1)], k=[0,1,2,3,4,5,6,7])

create_controller()