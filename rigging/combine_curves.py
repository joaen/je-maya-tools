import pymel.core as pm

selected_curves = pm.ls(selection=True)
shape_nodes = pm.listRelatives(selected_curves, s=True)

pm.makeIdentity(selected_curves, apply=True, t=True, r=True, s=True)
null_group = pm.group(em=True, name="newCtrl")
pm.parent(shape_nodes, null_group, s=True, r=True)

pm.delete(selected_curves)
pm.delete(shape_nodes, constructionHistory=True)


pm.circle(normal=(1,0,1), center=(0,0,0))
pm.circle(normal=(1,0,0), center=(0,0,0))
pm.circle(normal=(0,0,1), center=(0,0,0))
