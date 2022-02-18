import pymel.core as pm

def combine_curves(curves):
    selected_curves = curves
    shape_nodes = pm.listRelatives(selected_curves, s=True)
    null_group = pm.group(em=True, name="newCtrl")

    pm.makeIdentity(selected_curves, apply=True, t=True, r=True, s=True)
    pm.parent(shape_nodes, null_group, shape=True, relative=True)
    pm.delete(selected_curves)
    pm.delete(shape_nodes, constructionHistory=True)

def control_sphere():
    # Create 7 circles that form a sphere
    circle0 = pm.circle(normal=(1,0,0), center=(0,0,0))[0]
    circle1 = pm.circle(normal=(1,0,0), center=(0,0,0))[0]
    circle2 = pm.circle(normal=(1,0,0), center=(0,0,0))[0]
    circle3 = pm.circle(normal=(0,0,1), center=(0,0,0))[0]
    circle4 = pm.circle(normal=(0,1,0), center=(0,0,0))[0]
    circle5 = pm.circle(normal=(0,1,0), center=(0,0,0))[0]
    circle6 = pm.circle(normal=(0,1,0), center=(0,0,0))[0]

    # Translate, rotate and scale circles
    move_rotate_scale(circle0, [0,0,0], [0,45,0], [1,1,1])
    move_rotate_scale(circle1, [0,0,0], [0,-45,0], [1,1,1])
    move_rotate_scale(circle5, [0,0.7,0], [0,0,0], [0.7,0.7,0.7])
    move_rotate_scale(circle6, [0,-0.7,0], [0,0,0], [0.7,0.7,0.7])

    # Combine to one single shape
    combine_curves([circle0, circle1, circle2, circle3, circle4, circle5, circle6])

def move_rotate_scale(obj, tran, rot, scale):
    obj.setTranslation(tran)
    obj.setRotation(rot)
    obj.setScale(scale)


control_sphere()


