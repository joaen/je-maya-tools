'''
Name: ctrl_creator
Description: A tool for creating and editing rig controllers in Maya.
 
Author: Joar Engberg 2022
Installation:
Add ctrl_creator.py to your Maya scripts folder (Username\Documents\maya\scripts).
To start the tool within Maya, run these this lines of code from the Maya script editor or add them to a shelf button:

import ctrl_creator
ctrl_creator.start()
 
'''
import sys
import pymel.core as pm
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtCore, QtGui, QtWidgets
from functools import partial
from collections import OrderedDict 


def maya_main_window():
    # Return the Maya main window as QMainWindow
    main_window = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window), QtWidgets.QWidget) # type: ignore

class CtrlCreatorWindow(QtWidgets.QDialog):

    color_dict = OrderedDict([
        ("black", 0), ("darkblue", 5), ("blue", 6), ("cyan", 18), ("magenta", 9),
        ("red", 13), ("orange", 24), ("yellow", 17), ("lime", 14), ("white", 16)])
    
    color_dict_list = list(color_dict)

    def __init__(self):
        super(CtrlCreatorWindow, self).__init__(maya_main_window())
        self.setWindowTitle("Ctrl Creator")
        
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.resize(380, 250)
        self.create_ui_widgets()
        self.create_ui_layout()
        self.create_ui_connections()

        if pm.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)
 
    def create_ui_widgets(self):
        self.create_label = QtWidgets.QLabel("Create controllers")
        self.create_label.setStyleSheet("background-color: #5d5d5d; border: 1px solid #5d5d5d; border-radius: 2px;font-weight: bold;")
        self.create_label.setFixedHeight(20)

        self.edit_label = QtWidgets.QLabel("Edit controllers")
        self.edit_label.setStyleSheet("background-color: #5d5d5d; border: 1px solid #5d5d5d; border-radius: 2px;font-weight: bold;")
        self.edit_label.setFixedHeight(20)

        self.circle_button = QtWidgets.QPushButton(QtGui.QIcon(":circle.png"), "Circle")
        self.sphere_button = QtWidgets.QPushButton(QtGui.QIcon(":sphere.png"), "Sphere")
        self.square_button = QtWidgets.QPushButton(QtGui.QIcon(":square.png"), "Square")
        self.cube_button = QtWidgets.QPushButton(QtGui.QIcon(":cube.png"), "Cube")
        
        self.constraint_checkbox = QtWidgets.QCheckBox("ParentConstraint")
        self.lock_attr_checkbox = QtWidgets.QCheckBox("Hide + lock unused attrs")
        self.add_suffix_checkbox = QtWidgets.QCheckBox("_FK suffix")

        self.scale_label = QtWidgets.QLabel("Scale:")
        self.scale_up_button = QtWidgets.QPushButton("+")
        self.scale_up_button.setFixedWidth(30)
        self.scale_down_button = QtWidgets.QPushButton("-")
        self.scale_down_button.setFixedWidth(30)
        self.rotate_label = QtWidgets.QLabel("Rotate:")
        self.rotate_x_button = QtWidgets.QPushButton("X")
        self.rotate_x_button.setFixedWidth(30)
        self.rotate_y_button = QtWidgets.QPushButton("Y")
        self.rotate_y_button.setFixedWidth(30)
        self.rotate_z_button = QtWidgets.QPushButton("Z")
        self.rotate_z_button.setFixedWidth(30)

        # Create color buttons based on the color button dict
        self.color_button_list = []
        for n in range(0, 10):
            color_button = QtWidgets.QPushButton()
            color_button.setStyleSheet("background-color: {}".format(str(self.color_dict_list[n])))
            self.color_button_list.append(color_button)

    def create_ui_layout(self):
        checkbox_layout = QtWidgets.QHBoxLayout()
        checkbox_layout.setContentsMargins(0,0,0,20)
        checkbox_layout.addWidget(self.constraint_checkbox)
        checkbox_layout.addWidget(self.lock_attr_checkbox)
        checkbox_layout.addWidget(self.add_suffix_checkbox)

        create_layout = QtWidgets.QHBoxLayout()
        create_layout.addWidget(self.circle_button)
        create_layout.addWidget(self.sphere_button)
        create_layout.addWidget(self.square_button)
        create_layout.addWidget(self.cube_button)

        edit_layout = QtWidgets.QHBoxLayout()
        edit_layout.addWidget(self.rotate_label)
        edit_layout.addWidget(self.rotate_x_button)
        edit_layout.addWidget(self.rotate_y_button)
        edit_layout.addWidget(self.rotate_z_button)
        edit_layout.addWidget(self.scale_label)
        edit_layout.addWidget(self.scale_up_button)
        edit_layout.addWidget(self.scale_down_button)

        color_layout = QtWidgets.QHBoxLayout()
        color_layout.setSpacing(0)
        for btn in self.color_button_list:
            color_layout.addWidget(btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(self.create_label)
        main_layout.addLayout(create_layout)
        main_layout.addLayout(checkbox_layout)
        main_layout.addWidget(self.edit_label)
        main_layout.addLayout(edit_layout)
        main_layout.addLayout(color_layout)
        main_layout.addStretch()
 
    def create_ui_connections(self):
        self.circle_button.clicked.connect(partial(self.create_controller, "circle"))
        self.sphere_button.clicked.connect(partial(self.create_controller, "sphere"))
        self.square_button.clicked.connect(partial(self.create_controller, "square"))
        self.cube_button.clicked.connect(partial(self.create_controller, "cube"))

        self.rotate_x_button.clicked.connect(partial(self.rotate_ctrl_shape, [45, 0, 0]))
        self.rotate_y_button.clicked.connect(partial(self.rotate_ctrl_shape, [0, 45, 0]))
        self.rotate_z_button.clicked.connect(partial(self.rotate_ctrl_shape, [0, 0, 45]))

        self.scale_up_button.clicked.connect(partial(self.scale_ctrl_shape, 1.2))
        self.scale_down_button.clicked.connect(partial(self.scale_ctrl_shape, 0.8))

        for n in range(0, 10):
            index = self.color_dict.get(self.color_dict_list[n])
            self.color_button_list[n].clicked.connect(partial(self.set_ctrl_color, index))

    
    def get_cvs(self, object):
        children = pm.listRelatives(object, children=True)
        ctrl_vertices = []
        for c in children:
            spans = int(pm.getAttr(c+".spans"))
            vertices = "{shape}.cv[0:{count}]".format(shape=c, count=spans)
            ctrl_vertices.append(vertices)
        return ctrl_vertices

    def create_controller(self, input_shape):
        new_shapes_list = []
        for transform in pm.selected():
            if input_shape == "circle":
                shape = self.create_circle()
            elif input_shape == "sphere":
                shape = self.create_sphere()
            elif input_shape == "square":
                shape = self.create_square()
            elif input_shape == "cube":
                shape = self.create_cube()

            pm.rename(shape, transform+"_CTRL")
            offset_grp = pm.group(shape)
            pm.rename(offset_grp, transform+"_CTRL_Grp")
            pm.matchTransform(offset_grp, transform)
            new_shapes_list.append(shape)
        pm.select(new_shapes_list, replace=True)

    def scale_ctrl_shape(self, size):
        stored_selection = pm.selected()

        for ctrl in pm.selected():
            pm.select(self.get_cvs(ctrl), replace=True)
            pm.scale(size, size, size)
        
        pm.select(clear=True)
        for sel in stored_selection:
            pm.select(sel, add=True)

    def rotate_ctrl_shape(self, degrees):
        stored_selection = pm.selected()

        for ctrl in pm.selected():
            ctrl_pivot = pm.xform(ctrl, query=True, translation=True, worldSpace=True)
            pm.select(self.get_cvs(ctrl), replace=True)
            pm.rotate(degrees, relative=True, pivot=(ctrl_pivot))

        pm.select(clear=True)
        for sel in stored_selection:
            pm.select(sel, add=True)

    def create_sphere(self):
        # Create circles
        circles = []
        for n in range(0, 5):
            circles.append(pm.circle(normal=(0,0,0), center=(0,0,0))[0])

        circles[0].setRotation([0, 45, 0])
        circles[1].setRotation([0, -45, 0])
        circles[2].setRotation([0, -90, 0])
        circles[3].setRotation([90, 0, 0])
        
        # Combine circles into a sphere
        shape_nodes = pm.listRelatives(circles, shapes=True)
        output_node = pm.group(empty=True)
        pm.makeIdentity(circles, apply=True, t=True, r=True, s=True)
        pm.parent(shape_nodes, output_node, shape=True, relative=True)
        pm.delete(shape_nodes, constructionHistory=True)
        pm.delete(circles)
        return output_node

    def set_ctrl_color(self, color_index):
        selection = pm.selected()
        for obj in selection:
            shape_nodes = pm.listRelatives(obj, shapes=True)

            for shape in shape_nodes:
                pm.setAttr("{0}.overrideEnabled".format(shape), True)
                pm.setAttr("{0}.overrideColor".format(shape), color_index)
        pm.select(deselect=True)

    def create_circle(self):
        return pm.circle(normal=(1, 0, 0), center=(0, 0, 0))[0]

    def create_cube(self):
        return pm.curve(name="shape123", d=1, p=[(-1, -1, 1), (-1, 1, 1), (1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, -1, -1), (-1, 1, -1), (-1, 1, 1), (-1, 1, -1), (1, 1, -1), (1, -1, -1), (-1, -1, -1), (1, -1, -1), (1, -1, 1), (1, 1, 1), (1, 1, -1)], k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

    def create_square(self):
        return pm.curve(d=1, p=[(-1, 0, 1), (-1, 0, 1), (0, 0, 1), (1, 0, 1), (1, 0, 1), (1, 0, -1), (-1, 0, -1), (-1, 0, 1)], k=[0,1,2,3,4,5,6,7])

def start():
    global ctrl_creator_ui
    try:
        ctrl_creator_ui.close()
        ctrl_creator_ui.deleteLater()
    except:
        pass
    ctrl_creator_ui = CtrlCreatorWindow()
    ctrl_creator_ui.show()

if __name__ == "__main__":
    start()