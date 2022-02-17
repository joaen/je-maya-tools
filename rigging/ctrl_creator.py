from select import select
import pymel.core as pm


def get_cvs(object):
    spans = str(pm.getAttr(object+".spans") - 1)
    ctrl_vertices = "{shape}.cv[0:{count}]".format(shape=object, count=spans)
    return ctrl_vertices

def create_ctrl_shape():
    for transform in pm.selected():
        shape_name = transform
        shape = pm.circle (normal=(1, 0, 0), center=(0, 0, 0), name=shape_name+"_ctrl")
        offset_grp = pm.group(shape, name=shape_name+"_offset_grp")
        pm.matchTransform(offset_grp, transform)

# create_ctrl_shape()

def scale_ctrl_shape(size):
    stored_selection = pm.ls(selection=True)

    for ctrl in pm.selected():
        pm.select(get_cvs(ctrl), replace=True)
        pm.scale(size, size, size)
    
    pm.select(clear=True)
    for sel in stored_selection:
        pm.select(sel, add=True)

# scale_ctrl_shape(3)

def rotate_ctrl_shape(degrees):
    stored_selection = pm.ls(selection=True)

    for ctrl in pm.selected():
        ctrl_pivot = pm.xform(ctrl, query=True, translation=True, worldSpace=True)
        pm.select(get_cvs(ctrl), replace=True)
        pm.rotate(degrees, relative=True, pivot=(ctrl_pivot))

    pm.select(clear=True)
    for sel in stored_selection:
        pm.select(sel, add=True)




# rotate_ctrl_shape((0,0,0))