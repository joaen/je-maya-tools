import pymel.core as pm

selected_curves = pm.ls(selection=True)
shape_nodes = pm.listRelatives(selected_curves, s=True)

pm.makeIdentity(selected_curves, apply=True, t=True, r=True, s=True)
null_group = pm.group(em=True, name="newCtrl")
pm.parent(shape_nodes, null_group, s=True, r=True)

pm.delete(selected_curves)
pm.delete(shape_nodes, constructionHistory=True)

import pymel.core as pm

# 45s
pm.rotate(pm.circle(normal=(1,0,0), center=(0,0,0)), 0,45,0)
pm.rotate(pm.circle(normal=(1,0,0), center=(0,0,0)), 0,-45,0)

# straight
pm.circle(normal=(1,0,0), center=(0,0,0))
pm.circle(normal=(0,0,1), center=(0,0,0))

# flat
pm.circle(normal=(0,1,0), center=(0,0,0))
pm.scale(pm.move(0,0.7,0, pm.circle(normal=(0,1,0), center=(0,0,0))), 0.7,0.7,0.7)
pm.scale(pm.move(0,-0.7,0, pm.circle(normal=(0,1,0), center=(0,0,0))), 0.7,0.7,0.7)



# #STUFFFFF
# # THIS?
# pm.scale(pm.move(0,0.7,0, pm.circle(normal=(0,1,0), center=(0,0,0))), 0.7,0.7,0.7)
# pm.scale(pm.move(0,-0.7,0, pm.circle(normal=(0,1,0), center=(0,0,0))), 0.7,0.7,0.7)

# # OR THIS?
# circle = pm.circle(normal=(0,1,0), center=(0,0,0))
# pm.move(0,0.7,0, circle)
# pm.scale(circle, 0.7,0.7,0.7)

# circle = pm.circle(normal=(0,1,0), center=(0,0,0))
# pm.move(0,-0.7,0, circle)
# pm.scale(circle, 0.7,0.7,0.7)

