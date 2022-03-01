import maya.mel as mel
import maya.cmds as cmds

joints = []
dupes = []

mel.eval("nurbsPlane -p 0 0 0 -ax 0 0 1 -w 1 -lr 50 -d 3 -u 1 -v 5 -ch 1; objectMoveCommand;")  
mel.eval("rebuildSurface -ch 1 -rpo 1 -rt 0 -end 1 -kr 0 -kcp 0 -kc 1 -su 1 -du 1 -sv 5 -dv 3 -tol 0.01 -fr 0 -dir 0;")
mel.eval("createHair 1 5 10 0 0 0 0 5 0 2 1 1;")

curves = cmds.listRelatives("hairSystem1OutputCurves", children=True)

cmds.select(clear=True)
for i in curves:
    cmds.select(i, add=True)
cmds.select("hairSystem1OutputCurves", add=True)
cmds.select("hairSystem1", add=True)
cmds.select("nucleus1", add=True)
cmds.delete()

folliclesList = cmds.listRelatives("hairSystem1Follicles", children=True)
for i in folliclesList:
    jnt = cmds.joint(p=(0, 0, 0))

    joints.append(jnt)

    cmds.parent(jnt, i)
    cmds.xform(jnt, t=(0, 0, 0) )

    dupe = cmds.duplicate(jnt)[0]
    dupes.append(dupe)
    cmds.parent(dupe, world=True)

cmds.skinCluster(dupes, "nurbsPlane1")

for i in dupes:
    cmds.rename(i, "BindToPlane#")

for i in joints:
    cmds.rename(i, "BindToGeo#")