import pymel.core as pm


def get_cvs(object):
    spans = str(pm.getAttr(object+".spans") - 1)
    ctrl_vertices = "{shape}.cv[0:{count}]".format(shape=object, count=spans)
    return ctrl_vertices

def create_controller():
    for transform in pm.selected():
        shape = get_cube()
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

def combine_curves(curves):
    shape_nodes = pm.listRelatives(curves, s=True)
    output_node = pm.group(em=True, name="newCtrl")
    pm.makeIdentity(curves, apply=True, t=True, r=True, s=True)
    pm.parent(shape_nodes, output_node, shape=True, relative=True)
    pm.delete(curves)
    pm.delete(shape_nodes, constructionHistory=True)
    return output_node

def get_sphere():
    # Create circles and add to list
    circles = []
    for n in range(0, 7):
        circles.append(pm.circle(normal=(0,0,0), center=(0,0,0))[0])

    # Translate, rotate and scale circles
    move_rotate_scale(circles[0], [0,0,0], [0,45,0], [1,1,1])
    move_rotate_scale(circles[1], [0,0,0], [0,-45,0], [1,1,1])
    move_rotate_scale(circles[2], [0,0,0], [0,0,0], [1,1,1])
    move_rotate_scale(circles[3], [0,0,0], [0,-90,0], [1,1,1])
    move_rotate_scale(circles[4], [0,0,0], [90,0,0], [1,1,1])
    move_rotate_scale(circles[5], [0,0.7,0], [90,0,0], [0.7,0.7,0.7])
    move_rotate_scale(circles[6], [0,-0.7,0], [90,0,0], [0.7,0.7,0.7])
    
    # Combine to one single shape
    new_sphere = combine_curves(circles)
    return new_sphere


def move_rotate_scale(obj, tran, rot, scale):
    obj.setTranslation(tran)
    obj.setRotation(rot)
    obj.setScale(scale)

def get_circle():
    return pm.circle(normal=(1, 0, 0), center=(0, 0, 0))

def get_cube():
    top_square = get_square([0,1,0])
    top_square.setTranslation([0,0.5,0])
    bottom_square = get_square([0,1,0])
    bottom_square.setTranslation([0,-0.5,0])

    c1= pm.curve(degree=1, p=[(0.5, 0.5, 0.5), (0.5, -0.5, 0.5)], k=[0,1])
    c2 = pm.curve(degree=1, p=[(0.5, 0.5, -0.5), (0.5, -0.5, -0.5)], k=[0,1])
    c3 = pm.curve(degree=1, p=[(-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5)], k=[0,1])
    c4 = pm.curve(degree=1, p=[(-0.5, 0.5, 0.5), (-0.5, -0.5, 0.5)], k=[0,1])

    new_cube = combine_curves([top_square, bottom_square, c1, c2, c3, c4])
    return new_cube

def get_square(normal_axis):
    square = pm.nurbsSquare(normal=(normal_axis), center=(0, 0, 0))
    curves = pm.listRelatives(square, children=True)
    new_square = combine_curves(curves)
    pm.delete(square[0])
    return new_square

create_controller()