import maya.cmds as cmds


def createRollJoints():
    # Select start and end joint
    selectedObjects = cmds.ls(selection=True)

    # Multiply Divide node name
    MDNName = selectedObjects[0] + '_Twist_MDN'

    # Name for the twist drivers
    startJntName = selectedObjects[0] + '_TwistDrive_Start'
    endJntName = selectedObjects[0] + '_TwistDrive_End'

    # Name for the roll joints
    r1 = selectedObjects[0] + '_Roll1'
    r2 = selectedObjects[0] + '_Roll2'
    r3 = selectedObjects[0] + '_Roll3'

    # Name for IK handle
    ikHandleName = selectedObjects[0] + '_Twist_IKHandle'

    # Duplicate start joint three times to create roll joints
    jnt3 = cmds.duplicate(selectedObjects[0], name=r1, po=True)
    jnt2 = cmds.duplicate(selectedObjects[0], name=r2, po=True)
    jnt1 = cmds.duplicate(selectedObjects[0], name=r3, po=True)

    # Duplicate start joint two times to create start driver and end driver
    driveJntStart = cmds.duplicate(selectedObjects[0], name=startJntName, po=True)
    driveJntEnd = cmds.duplicate(selectedObjects[0], name=endJntName, po=True)

    # Parent constraint joints into correct position
    pc1 = cmds.parentConstraint(selectedObjects[0], jnt1, w=0)
    pc2 = cmds.parentConstraint(selectedObjects[1], jnt1, w=1)
    pc3 = cmds.parentConstraint(selectedObjects[0], jnt2, w=0.2)
    pc4 = cmds.parentConstraint(selectedObjects[1], jnt2, w=0.6)
    pc5 = cmds.parentConstraint(selectedObjects[0], jnt3, w=1)
    pc6 = cmds.parentConstraint(selectedObjects[1], jnt3, w=1)
    driveJnt1 = cmds.parentConstraint(selectedObjects[0], driveJntStart, w=1)
    driveJnt2 = cmds.parentConstraint(selectedObjects[0], driveJntStart, w=1)
    driveJnt3 = cmds.parentConstraint(selectedObjects[1], driveJntEnd, w=1)
    driveJnt4 = cmds.parentConstraint(selectedObjects[1], driveJntEnd, w=1)

    # Delete the constraints
    cmds.delete(pc1, pc3, pc5, driveJnt1, driveJnt3)

    # Make the roll joints bigger
    cmds.setAttr(r1 + '.radius', 2)
    cmds.setAttr(r2 + '.radius', 2)
    cmds.setAttr(r3 + '.radius', 2)

    # Parent the joints 
    cmds.parent(r1, selectedObjects[0])
    cmds.parent(r2, selectedObjects[0])
    cmds.parent(r3, selectedObjects[0])
    cmds.parent(startJntName, selectedObjects[0])
    cmds.parent(endJntName, selectedObjects[0])
    cmds.parent(endJntName, startJntName)

    # Create an IK handle to drive the roll joints
    cmds.ikHandle(startJoint=startJntName, endEffector=endJntName, p=1, w=1, solver='ikSCsolver', name=ikHandleName)
    
    # Create mutiply divide node
    cmds.createNode('multiplyDivide', name=MDNName)
    
    # Set the influence of each roll joint (Basically what value each roll joint will mutiply with)
    cmds.setAttr('.input2X', 0.3)
    cmds.setAttr('.input2Y', 0.6)
    cmds.setAttr('.input2Z', 0.8)

    # Connect so the rotation of the start joint affect every roll joint
    cmds.connectAttr(startJntName+'.rotateX', MDNName+'.input1X')
    cmds.connectAttr(startJntName+'.rotateX', MDNName+'.input1Y')
    cmds.connectAttr(startJntName+'.rotateX', MDNName+'.input1Z')
    cmds.connectAttr(MDNName+'.outputX', r1+'.rotateX')
    cmds.connectAttr(MDNName+'.outputY', r2+'.rotateX')
    cmds.connectAttr(MDNName+'.outputZ', r3+'.rotateX')

    # Parent IK handle to the end joint
    cmds.parent(ikHandleName, selectedObjects[1])


createRollJoints()

