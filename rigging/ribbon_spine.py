import maya.mel as mel
import maya.cmds as cmds

def create_ribbonspone():
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

def create_ribbon():
    selection = cmds.ls(selection=True)
    point_list = []
    joints = []
    dupes = []

    for j in selection:
        joint_pos = cmds.xform(j, query=True, translation=True, worldSpace=True)
        point_list.append(joint_pos)
    
    # point_list.append((0,0,0))
    # point_list.append((0,1,0))
    # Create plane
    curve = cmds.curve(degree=3, point=point_list)
    curve_dupe = cmds.duplicate(curve)
    cmds.move(1, 0, 0, curve, relative=True, objectSpace=True, worldSpaceDistance=True)
    cmds.move(-1, 0, 0, curve_dupe, relative=True, objectSpace=True, worldSpaceDistance=True)
    
    # plane = cmds.loft(curve_dupe, curve, constructionHistory=False, range=False, autoReverse=True)
    # cmds.delete(curve, curve_dupe)

    # Create hair
    # cmds.select(plane, replace=True)
    # mel.eval("createHair 1 5 10 0 0 0 0 5 0 2 1 1;")  
    # cmds.delete("hairSystem1OutputCurves", "hairSystem1", "nucleus1")

    # # Create joints
    # folliclesList = cmds.listRelatives("hairSystem1Follicles", children=True)
    # for i in folliclesList:
    #     jnt = cmds.joint(p=(0, 0, 0))

    #     joints.append(jnt)

    #     cmds.parent(jnt, i)
    #     cmds.xform(jnt, t=(0, 0, 0) )

    #     dupe = cmds.duplicate(jnt)[0]
    #     dupes.append(dupe)
    #     cmds.parent(dupe, world=True)

    # cmds.skinCluster(dupes, plane)

    # for i in dupes:
    #     cmds.rename(i, "BindToPlane#")

    # for i in joints:
    #     cmds.rename(i, "BindToGeo#")



create_ribbon()