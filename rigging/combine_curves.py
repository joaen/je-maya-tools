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
    combine_curves(circles)

def move_rotate_scale(obj, tran, rot, scale):
    obj.setTranslation(tran)
    obj.setRotation(rot)
    obj.setScale(scale)


control_sphere()


