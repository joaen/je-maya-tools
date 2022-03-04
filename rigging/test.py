# import maya.api.OpenMaya as om
import maya.cmds as cmds

cmds.matchTransform("locator1", "conan_rig:FKWrist_L")
cmds.rotate("90deg", "180deg", "0deg", "locator1", relative=True, objectSpace=True)
cmds.matchTransform("conan_rig:IKArm_L", "locator1")
