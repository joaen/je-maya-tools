'''
Name: ikfk_matching
Description: Universal ikfk matching tool for Maya, which is compatible with most character rigs.
The tool is used to switch between ik and fk seamlessly without compromising the current pose. 
 
Author: Joar Engberg 2022

Installation:
Add ikfk_matching.py to your Maya scripts folder.
PC: (Username\Documents\maya\scripts).
Mac: (Library\Preferences\Autodesk\maya\scripts)

To start the tool in Maya execute these lines in the script editor (or add them to a shelf button):

import ikfk_matching
ikfk_matching.start()

'''

from collections import OrderedDict
from functools import partial
import sys
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtCore, QtGui, QtWidgets
import json
import maya.api.OpenMaya as om
import maya.mel as mel


def maya_main_window():
    # Return the Maya main window as QMainWindow
    main_window = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window), QtWidgets.QWidget) # type: ignore

class TemplateToolWindow(QtWidgets.QDialog):
    def __init__(self):
        super(TemplateToolWindow, self).__init__(maya_main_window())
        self.setWindowTitle("ikfk_matching")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.resize(280, 120)
        self.create_ui_widgets()
        self.create_ui_layout()
        self.create_ui_connections()

        if cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)
 
    def create_ui_widgets(self):
        self.template_button1 = QtWidgets.QPushButton("RIGHT ARM")
        self.template_button1.setStyleSheet("background-color: lightgreen; color: black")
        self.template_button2 = QtWidgets.QPushButton("LEFT ARM")
        self.template_button2.setStyleSheet("background-color: deepskyblue; color: black")
        self.template_button3 = QtWidgets.QPushButton("RIGHT LEG")
        self.template_button3.setStyleSheet("background-color: lightgreen; color: black")
        self.template_button4 = QtWidgets.QPushButton("LEFT LEG")
        self.template_button4.setStyleSheet("background-color: deepskyblue; color: black")
        self.template_checkbox = QtWidgets.QCheckBox("TEMPLATE_CHECKBOX")
        self.template_combobox = QtWidgets.QComboBox()
        self.template_combobox.addItem("TEMPLATE_COMBOBOX_ITEM")
        self.template_textfield = QtWidgets.QLineEdit()
        self.template_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)

        # setting background color to push button when mouse hover over it
        icon_button_css = (
            "QPushButton { background-color: #444444; border: transparent; border-radius: 12px; }"
            "QPushButton:hover { background-color: #5D5D5D; }"
            "QPushButton:pressed {background-color: black; }")
        
        self.settings1_button = QtWidgets.QPushButton()
        self.settings1_button.setIcon(QtGui.QIcon(":advancedSettings.png"))
        self.settings1_button.setFixedSize(24, 24)
        self.settings1_button.setStyleSheet(icon_button_css)

        self.settings2_button = QtWidgets.QPushButton()
        self.settings2_button.setIcon(QtGui.QIcon(":advancedSettings.png"))
        self.settings2_button.setFixedSize(24, 24)
        self.settings2_button.setStyleSheet(icon_button_css)

        self.settings3_button = QtWidgets.QPushButton()
        self.settings3_button.setIcon(QtGui.QIcon(":advancedSettings.png"))
        self.settings3_button.setFixedSize(24, 24)
        self.settings3_button.setStyleSheet(icon_button_css)

        self.settings4_button = QtWidgets.QPushButton()
        self.settings4_button.setIcon(QtGui.QIcon(":advancedSettings.png"))
        self.settings4_button.setFixedSize(24, 24)
        self.settings4_button.setStyleSheet(icon_button_css)

        self.help_icon_button = QtWidgets.QPushButton()
        self.help_icon_button.setIcon(QtGui.QIcon(":help.png"))
        self.help_icon_button.setFixedSize(24, 24)
        self.help_icon_button.setStyleSheet(icon_button_css)

        self.close_button = QtWidgets.QPushButton("Close")
        self.close_button.setFixedWidth(100)

        self.hide_checkbox = QtWidgets.QCheckBox("Show settings")

        self.settings1_button.setVisible(False)
        self.settings2_button.setVisible(False)
        self.settings3_button.setVisible(False)
        self.settings4_button.setVisible(False)
        

    def create_ui_layout(self):
        horizontal_layout1 = QtWidgets.QHBoxLayout()
        horizontal_layout1.addWidget(self.settings1_button)
        horizontal_layout1.addWidget(self.template_button1)

        horizontal_layout2 = QtWidgets.QHBoxLayout()
        horizontal_layout2.addWidget(self.settings2_button)
        horizontal_layout2.addWidget(self.template_button2)

        horizontal_layout3 = QtWidgets.QHBoxLayout()
        horizontal_layout3.addWidget(self.settings3_button)
        horizontal_layout3.addWidget(self.template_button3)

        horizontal_layout4 = QtWidgets.QHBoxLayout()
        horizontal_layout4.addWidget(self.settings4_button)
        horizontal_layout4.addWidget(self.template_button4)

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addLayout(horizontal_layout1)
        vertical_layout.addLayout(horizontal_layout2)
        vertical_layout.addLayout(horizontal_layout3)
        vertical_layout.addLayout(horizontal_layout4)

        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addWidget(self.help_icon_button)
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(self.hide_checkbox)
        horizontal_layout.addWidget(self.close_button)

        top_label = QtWidgets.QLabel("Toggle IK/FK:")
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)
        main_layout.addWidget(top_label)
        main_layout.addLayout(vertical_layout)
        main_layout.addLayout(horizontal_layout2)
        main_layout.addSpacing(30)
        main_layout.addLayout(horizontal_layout)
 
    def create_ui_connections(self):
        self.settings1_button.clicked.connect(partial(self.open_settings_window, "RightArm"))
        self.settings2_button.clicked.connect(partial(self.open_settings_window, "LeftArm"))
        self.settings3_button.clicked.connect(partial(self.open_settings_window, "RightLeg"))
        self.settings4_button.clicked.connect(partial(self.open_settings_window, "LeftLeg"))

        self.template_button1.clicked.connect(partial(self.match_ikfk, "RightArm"))
        self.template_button2.clicked.connect(partial(self.match_ikfk, "LeftArm"))
        self.template_button3.clicked.connect(partial(self.match_ikfk, "RightLeg"))
        self.template_button4.clicked.connect(partial(self.match_ikfk, "LeftLeg"))

        self.hide_checkbox.clicked.connect(self.toggle_settings)
        self.close_button.clicked.connect(self.close_ikfk_window)

    def toggle_settings(self):
        if self.hide_checkbox.isChecked() == True:
            self.settings1_button.setVisible(True)
            self.settings2_button.setVisible(True) 
            self.settings3_button.setVisible(True) 
            self.settings4_button.setVisible(True)
        elif self.hide_checkbox.isChecked() == False:
            self.settings1_button.setVisible(False)
            self.settings2_button.setVisible(False) 
            self.settings3_button.setVisible(False) 
            self.settings4_button.setVisible(False)

    def close_ikfk_window(self):
        self.close()
        self.deleteLater()

    def open_settings_window(self, limb_name):
        try:
            self.settings_window.close()
            self.settings_window.deleteLater()
        except:
            pass
        self.settings_window = SettingsWindow(limb_name)
        self.settings_window.show()

    def get_pole_position(self, start_joint, mid_joint, end_joint, offset):
        # Get joint poistions as vectors
        joint1_pos = om.MVector(cmds.xform(start_joint, query=True, worldSpace=True, translation=True))
        joint2_pos = om.MVector(cmds.xform(mid_joint, query=True, worldSpace=True, translation=True))
        joint3_pos = om.MVector(cmds.xform(end_joint, query=True, worldSpace=True, translation=True))

        # Calculate the mid point between joint1 and joint3
        mid_point_pos = joint1_pos + (joint3_pos - joint1_pos).normal() * ((joint3_pos - joint1_pos).length() * 0.5)

        # Get the pole vector position by aiming from the mid point towards joint2 position. Scale the vector using the offset float.
        pole_vec = mid_point_pos + (joint2_pos - mid_point_pos).normal() * ((joint2_pos - mid_point_pos).length() * offset)
        
        return pole_vec

    def create_loc(self, start_joint, mid_joint, end_joint, offset=2):
        joint1 = start_joint
        joint2 = mid_joint
        joint3 = end_joint
        pole_vector_pos = self.get_pole_position(joint1, joint2, joint3, offset)
        loc = cmds.spaceLocator()
        cmds.move(pole_vector_pos[0], pole_vector_pos[1], pole_vector_pos[2], loc, absolute=True, worldSpace=True)
        return loc
    
    def match_ikfk(self, limb_name):
        output_file_path = cmds.internalVar(userPrefDir=True)+"ikfk_settings_{}.json".format(limb_name)
        settings_dict = json.load(open(output_file_path))
        print("Loaded settings from: "+output_file_path)

        ikfk_attr_name = settings_dict.get("IKFK_blend_attr")
        ikfk_attr_value = cmds.getAttr(ikfk_attr_name)
        fk_ctrl_start = settings_dict.get("FK_ctrl_start")
        fk_ctrl_mid = settings_dict.get("FK_ctrl_mid")
        fk_ctrl_end = settings_dict.get("FK_ctrl_end")
        ik_joint_start = settings_dict.get("IK_joint_start")
        ik_joint_mid = settings_dict.get("IK_joint_mid")
        ik_joint_end = settings_dict.get("IK_joint_end")
        ik_ctrl = settings_dict.get("IK_ctrl")
        ik_pole_ctrl = settings_dict.get("IK_pole_ctrl")
        ik_value = int(settings_dict.get("IK"))
        fk_value = int(settings_dict.get("FK"))

        if ikfk_attr_value == fk_value:
            cmds.setAttr(ikfk_attr_name, ik_value)
            cmds.matchTransform(ik_ctrl, fk_ctrl_end)

            offset_x = settings_dict.get("Offset X")+"deg"
            offset_y = settings_dict.get("Offset Y")+"deg"
            offset_z = settings_dict.get("Offset Z")+"deg"

            cmds.rotate(offset_x, offset_y, offset_z, ik_ctrl, relative=True, objectSpace=True)
            pole_locator = self.create_loc(fk_ctrl_start, fk_ctrl_mid, fk_ctrl_end, 2)
            cmds.matchTransform(ik_pole_ctrl, pole_locator)
            cmds.delete(pole_locator)

        elif ikfk_attr_value == ik_value:
            cmds.setAttr(ikfk_attr_name, fk_value)
            cmds.matchTransform(fk_ctrl_start, ik_joint_start, rotation=True)
            cmds.matchTransform(fk_ctrl_mid, ik_joint_mid, rotation=True)
            cmds.matchTransform(fk_ctrl_end, ik_joint_end, rotation=True)


class SettingsWindow(QtWidgets.QDialog):

    textfield_widget_dict = OrderedDict([
        ("IKFK_blend_attr", ""),
        ("IK", ""),
        ("FK", ""),
        ("FK_ctrl_start", ""),
        ("FK_ctrl_mid", ""),
        ("FK_ctrl_end", ""),
        ("IK_joint_start", ""),
        ("IK_joint_mid", ""),
        ("IK_joint_end", ""),
        ("IK_ctrl", ""),
        ("IK_pole_ctrl", ""),
        ("Offset X", ""),
        ("Offset Y", ""),
        ("Offset Z", "")
    ])

    output_data_dict = OrderedDict(textfield_widget_dict)

    def __init__(self, limb_name):
        super(SettingsWindow, self).__init__(maya_main_window())
        self.limb_name = limb_name
        self.output_file_path = cmds.internalVar(userPrefDir=True)+"ikfk_settings_{}.json".format(limb_name)
        self.setWindowTitle("Settings - "+limb_name)
        self.setWindowIcon(QtGui.QIcon(":advancedSettings.png"))
        
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.resize(400, 120)
        self.create_ui_layout()
        self.create_ui_connections()

        if cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

    def load_settings(self, limb_name):
        load_file_path = cmds.internalVar(userPrefDir=True)+"ikfk_settings_{}.json".format(limb_name)
        file_path = json.load(open(load_file_path))
        return file_path

    def copy_settings(self, limb_name):
        copied_dict = {}
        copied_dict = self.load_settings(limb_name)
        for key, widget in self.textfield_widget_dict.items():
            widget.setText(copied_dict[key])
        
    def create_ui_layout(self):
        self.action_dict = {}
        settings_dict = {}
        try:
            settings_dict = self.load_settings(self.limb_name)
        except:
            pass

        for key in self.textfield_widget_dict:
            label = QtWidgets.QLabel(str(key))
            textfield = QtWidgets.QLineEdit()
            try:
                textfield.setText(settings_dict[key])
            except:
                pass
            self.textfield_widget_dict[key] = textfield

        self.save_button = QtWidgets.QPushButton("Save settings")
        self.close_button = QtWidgets.QPushButton("Cancel")
        
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.close_button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        self.settings_label = QtWidgets.QLabel(str(self.limb_name))
        self.settings_label.setStyleSheet("background-color: #5d5d5d; border: 1px solid #5d5d5d; border-radius: 2px;font-weight: bold;")
        self.settings_label.setFixedHeight(20)
        main_layout.addWidget(self.settings_label)

        test_layout = QtWidgets.QHBoxLayout()
        attr_layout = QtWidgets.QHBoxLayout()
        for key in self.textfield_widget_dict:
            if key == "IKFK_blend_attr" or key == "IK" or key == "FK":
                label = QtWidgets.QLabel(str(key))
                attr_layout.addWidget(label)
                attr_layout.addWidget(self.textfield_widget_dict[key])
                main_layout.addLayout(attr_layout)
            elif key == "Offset X":
                degree_label = QtWidgets.QLabel("Rotation offset on IK controller (Degrees):")
                degree_label.setStyleSheet("background-color: #5d5d5d; border: 1px solid #5d5d5d; border-radius: 2px;font-weight: bold;")
                degree_label.setFixedHeight(20)
                label = QtWidgets.QLabel(str(key))
                test_layout.addWidget(label)
                test_layout.addWidget(self.textfield_widget_dict[key])
                main_layout.addSpacing(24)
                main_layout.addWidget(degree_label)
                main_layout.addLayout(test_layout)
                main_layout.addSpacing(24)
            elif key == "Offset Y" or key == "Offset Z":
                label = QtWidgets.QLabel(str(key))
                test_layout.addWidget(label)
                test_layout.addWidget(self.textfield_widget_dict[key])
                main_layout.addLayout(test_layout)
            else:
                label = QtWidgets.QLabel(str(key))
                label_layout = QtWidgets.QHBoxLayout()
                label_layout.addWidget(label)
                label_layout.addWidget(self.textfield_widget_dict[key])
                main_layout.addLayout(label_layout)
                action = self.textfield_widget_dict[key].addAction(QtGui.QIcon(":addCreateGeneric.png"), QtWidgets.QLineEdit.TrailingPosition)
                action.setToolTip("Add name from selected object")
                self.action_dict[key] = action
        
        self.attr_action = self.textfield_widget_dict["IKFK_blend_attr"].addAction(QtGui.QIcon(":addCreateGeneric.png"), QtWidgets.QLineEdit.TrailingPosition)
        self.attr_action.setToolTip("Add selected attribute from channelbox")

        self.textfield_widget_dict.get("IK").setFixedWidth(24)
        self.textfield_widget_dict.get("FK").setFixedWidth(24)
        self.textfield_widget_dict.get("IK").setText(str(0))
        self.textfield_widget_dict.get("FK").setText(str(0))
        self.textfield_widget_dict.get("Offset X").setText(str(0))
        self.textfield_widget_dict.get("Offset Y").setText(str(0))
        self.textfield_widget_dict.get("Offset Z").setText(str(0))

        search_row = QtWidgets.QHBoxLayout()
        self.keyword_label = QtWidgets.QLabel("Search for:")
        self.keyword_textfield = QtWidgets.QLineEdit()
        self.replace_label = QtWidgets.QLabel("Replace with:")
        self.replace_textfield = QtWidgets.QLineEdit()
        self.replace_button = QtWidgets.QPushButton()
        self.replace_button.setIcon(QtGui.QIcon(":renamePreset.png"))
        self.replace_button.setFixedSize(24, 24)
        search_row.addWidget(self.keyword_label)
        search_row.addWidget(self.keyword_textfield)
        search_row.addWidget(self.replace_label)
        search_row.addWidget(self.replace_textfield)
        search_row.addWidget(self.replace_button)

        copy_row = QtWidgets.QHBoxLayout()
        self.copy_label = QtWidgets.QLabel("Copy text from:")
        self.copy_label.setStyleSheet("background-color: #5d5d5d; border: 1px solid #5d5d5d; border-radius: 2px;font-weight: bold;")
        self.copy_label.setFixedHeight(20)
        self.copy_left_arm_button = QtWidgets.QPushButton("Left arm")
        self.copy_right_arm_button = QtWidgets.QPushButton("Right arm")
        self.copy_left_leg_button = QtWidgets.QPushButton("Left leg")
        self.copy_right_leg_button = QtWidgets.QPushButton("Right leg")

        copy_row.addWidget(self.copy_left_arm_button)
        copy_row.addWidget(self.copy_right_arm_button)
        copy_row.addWidget(self.copy_left_leg_button)
        copy_row.addWidget(self.copy_right_leg_button)

        main_layout.addWidget(self.copy_label)
        main_layout.addLayout(copy_row)
        main_layout.addLayout(search_row)
        main_layout.addSpacing(24)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
 
    def create_ui_connections(self):
        self.save_button.clicked.connect(self.save_settings)
        self.close_button.clicked.connect(self.close_settings)
        self.replace_button.clicked.connect(self.search_and_replace)

        self.copy_right_arm_button.clicked.connect(partial(self.copy_settings, "RightArm"))
        self.copy_left_arm_button.clicked.connect(partial(self.copy_settings, "LeftArm"))
        self.copy_right_leg_button.clicked.connect(partial(self.copy_settings, "RightLeg"))
        self.copy_left_leg_button.clicked.connect(partial(self.copy_settings, "LeftLeg"))

        for key, action in self.action_dict.items():
            action.triggered.connect(partial(self.selected_to_textfield, key))
        self.attr_action.triggered.connect(self.selected_attr_to_textfield)
    
    def selected_attr_to_textfield(self):
        selected_object = cmds.ls(selection=True)[0]
        main_channelbox = mel.eval('$temp=$gChannelBoxName')
        selected_channel = cmds.channelBox(main_channelbox, query=True, selectedMainAttributes=True)[0]
        self.textfield_widget_dict["IKFK_blend_attr"].setText("{}.{}".format(selected_object, selected_channel))

    def selected_to_textfield(self, textfield_key):
        selection = cmds.ls(selection=True)[0]
        self.textfield_widget_dict[textfield_key].setText(selection)

    def close_settings(self):
        self.close()
        self.deleteLater()

    def search_and_replace(self):
        keyword = self.keyword_textfield.text()
        replace_with = self.replace_textfield.text()

        for key, widget in self.textfield_widget_dict.items():
            if keyword in widget.text():
                new_string = widget.text().replace(keyword, replace_with)
                widget.setText(new_string)


    def save_settings(self):
        try:

            for key, value in self.textfield_widget_dict.iteritems():
                self.output_data_dict[key] = value.text()

            with open(self.output_file_path, "w") as outfile:
                json.dump(self.output_data_dict, outfile, indent=4)
            print("Saved settings: "+self.output_file_path)
            self.close()
            self.deleteLater()
        except Exception as error:
            print(error)
            cmds.warning("Can't save settings. Do you have permission to write to this file?")
            

def start():
    global template_tool_ui
    try:
        template_tool_ui.close()
        template_tool_ui.deleteLater()
    except:
        pass
    template_tool_ui = TemplateToolWindow()
    template_tool_ui.show()

if __name__ == "__main__":
    start()