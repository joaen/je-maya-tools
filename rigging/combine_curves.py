import pymel.core as pm
import maya.cmds as cmds

# out_node = pm.createNode("transform")
# for axis_normal in [[1,0,0], [0,1,0], [0,0,1]]:
#     obj = pm.circle(normal=axis_normal)
#     obj.setTranslation(axis_normal)
#     circle.setScale()
#     pm.makeIdentiy(circle, apply=True)
#     obj.getShape().setParent(out_node, shape=True)


def combine_curves(curves):
    pm.select(clear=True)
    for i in curves:
        pm.select(i, add=True)
    
    selected_curves = pm.ls(sl=True)
    shape_nodes = pm.listRelatives(selected_curves, s=True)

    pm.makeIdentity(selected_curves, apply=True, t=True, r=True, s=True)
    null_group = pm.group(em=True, name="newCtrl")

    pm.parent(shape_nodes, null_group, shape=True, relative=True)

    # pm.delete(shape_nodes, constructionHistory=True)
    # pm.delete(curves)
    # cmds.delete(selected_curves)
    # for i in selected_curves:
    #     pm.delete(i)
    # print(selected_curves)

def control_sphere():
    # 45s
    circle0 = pm.circle(normal=(1,0,0), center=(0,0,0))
    pm.rotate(circle0, 0,45,0)
    
    circle1 = pm.circle(normal=(1,0,0), center=(0,0,0))
    pm.rotate(circle1, 0,-45,0)

    # straight
    circle2 = pm.circle(normal=(1,0,0), center=(0,0,0))
    circle3 = pm.circle(normal=(0,0,1), center=(0,0,0))

    # flat 
    circle4 = pm.circle(normal=(0,1,0), center=(0,0,0))
    # pm.move(0,0.7,0, circle4)

    circle5 = pm.circle(normal=(0,1,0), center=(0,0,0))
    pm.move(0,-0.7,0, circle5)
    pm.scale(circle5, 0.7,0.7,0.7)
    pm.makeIdentity(circle5, apply=True, translate=True, rotate=True, scale=True)

    circle6 = pm.circle(normal=(0,1,0), center=(0,0,0))
    pm.move(0,0.7,0, circle6)
    pm.scale(circle6, 0.7,0.7,0.7)
    combine_curves([circle0, circle1, circle2, circle3, circle4, circle5, circle6])

control_sphere()


