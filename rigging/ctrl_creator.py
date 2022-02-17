import pymel.core as pm


def create_ctrl_shape():
    for transform in pm.selected (type="transform"):
        shape_name = transform
        shape = pm.circle (normal=(1, 0, 0), center=(0, 0, 0), name=shape_name+"_ctrl")
        offset_grp = pm.group(shape, name=shape_name+"_offset_grp")
        pm.matchTransform(offset_grp, transform)

def scale_ctrl_shape(size):
    sel = pm.selected()[0]
    spans = str(pm.getAttr(sel+".spans") - 1)
    ctrl_vertices = "{shape}.cv[0:{count}]".format(shape=sel, count=spans)
    pm.select(ctrl_vertices, replace=True)
    pm.scale(size, size, size)
    pm.select(sel, replace=True)

def rotate_ctrl_shape(degrees):
    shape_pivot = pm.xform (query=True, translation=True, worldSpace=True)
    sel = pm.selected()[0]
    spans = str(pm.getAttr(sel+".spans") - 1)
    ctrl_vertices = "{shape}.cv[0:{count}]".format(shape=sel, count=spans)
    pm.select(ctrl_vertices, replace=True)
    pm.rotate(degrees, relative=True, pivot=(shape_pivot))
    pm.select(sel, replace=True)

# create_ctrl_shape()
# scale_ctrl_shape(3)
# rotate_ctrl_shape((0,0,0))