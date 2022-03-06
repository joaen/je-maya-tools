from collections import OrderedDict
from functools import partial
import sys
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtCore, QtGui, QtWidgets
import json
import maya.api.OpenMaya as om


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
        self.setWindowTitle("IK/FK match")
        
        # self.output_file_path = cmds.internalVar(userPrefDir=True)+"{}_settings.json".format(limb_name)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.resize(364, 120)
        self.create_ui_widgets()
        self.create_ui_layout()
        self.create_ui_connections()

        if cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)
 
    def create_ui_widgets(self):
        self.template_label = QtWidgets.QLabel("match IK/FK:")

        self.template_button1 = QtWidgets.QPushButton("RIGHT ARM")
        self.template_button1.setStyleSheet("background-color: lightgreen; color: black")
        self.template_button1.setFixedWidth(120)
        self.template_button2 = QtWidgets.QPushButton("LEFT ARM")
        self.template_button2.setStyleSheet("background-color: salmon; color: black")
        self.template_button2.setFixedWidth(120)
        self.template_button3 = QtWidgets.QPushButton("RIGHT LEG")
        self.template_button3.setStyleSheet("background-color: lightgreen; color: black")
        self.template_button3.setFixedWidth(120)
        self.template_button4 = QtWidgets.QPushButton("LEFT LEG")
        self.template_button4.setStyleSheet("background-color: salmon; color: black")
        self.template_button4.setFixedWidth(120)

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
        # self.hide_checkbox.
        # self.hide_checkbox.setChecked(True)

        self.settings1_button.setVisible(False)
        self.settings2_button.setVisible(False)
        self.settings3_button.setVisible(False)
        self.settings4_button.setVisible(False)
        

    def create_ui_layout(self):

        horizontal_layout1 = QtWidgets.QHBoxLayout()
        # horizontal_layout1.setContentsMargins(30, 30, 30, 30)
        horizontal_layout1.addWidget(self.settings1_button)
        horizontal_layout1.addWidget(self.template_button1)
        horizontal_layout1.addSpacing(24)
        horizontal_layout1.addWidget(self.settings2_button)
        horizontal_layout1.addWidget(self.template_button2)

        horizontal_layout2 = QtWidgets.QHBoxLayout()
        horizontal_layout2.addWidget(self.settings3_button)
        horizontal_layout2.addWidget(self.template_button3)
        horizontal_layout2.addSpacing(24)
        horizontal_layout2.addWidget(self.settings4_button)
        horizontal_layout2.addWidget(self.template_button4)


        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addWidget(self.help_icon_button)
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(self.hide_checkbox)
        horizontal_layout.addWidget(self.close_button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)

        main_layout.addLayout(horizontal_layout1)
        main_layout.addLayout(horizontal_layout2)
        main_layout.addSpacing(30)
        main_layout.addStretch()
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
        # pass
 

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
        
        # print("Pole position: "+str(pole_vec))
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
        self.output_file_path = cmds.internalVar(userPrefDir=True)+"ikfk_settings_{}.json".format(limb_name)
        settings_dict = json.load(open(self.output_file_path))
        # Attritbute
        ikfk_attr_name = settings_dict.get("IKFK_blend_attr")
        print("Loaded settings from: "+self.output_file_path)
        # print(ikfk_attr_name)

        ikfk_attr_value = cmds.getAttr(ikfk_attr_name)

        # # FK

        fk_ctrl_start = settings_dict.get("FK_ctrl_start")
        fk_ctrl_mid = settings_dict.get("FK_ctrl_mid")
        fk_ctrl_end = settings_dict.get("FK_ctrl_end")
        
        ik_joint_start = settings_dict.get("IK_joint_start")
        ik_joint_mid = settings_dict.get("IK_joint_mid")
        ik_joint_end = settings_dict.get("IK_joint_end")

        # IK 
        ik_ctrl = settings_dict.get("IK_ctrl")
        ik_pole_ctrl = settings_dict.get("IK_pole_ctrl")

        # fk_joint_start = settings_dict.get("fk_joint_start")
        # fk_joint_mid = settings_dict.get("fk_joint_mid")
        # fk_joint_end = settings_dict.get("fk_joint_end")
        # print(settings_dict.get("FK"))
        # print(settings_dict.get("IK"))

        if ikfk_attr_value == int(settings_dict.get("FK")):
            # Set attribute
            cmds.setAttr(ikfk_attr_name, 0)

            # Create offset locator and move it to the target transform
            # offset_loc = cmds.spaceLocator()
            # cmds.matchTransform(offset_loc, fk_ctrl_end)


            # Match the ik ctrl transform with the offset transform
            cmds.matchTransform(ik_ctrl, fk_ctrl_end)

            # Add condition to add rotation
            if settings_dict.get("Offset X") == "":
                offset_x = "0deg"
            else:
                offset_x = settings_dict.get("Offset X")+"deg"

            if settings_dict.get("Offset Y") == "":
                offset_y = "0deg"
            else:
                offset_y = settings_dict.get("Offset Y")+"deg"

            if settings_dict.get("Offset Z") == "":
                offset_z = "0deg"
            else:
                offset_z = settings_dict.get("Offset Z")+"deg"
            
            cmds.rotate(offset_x, offset_y, offset_z, ik_ctrl, relative=True, objectSpace=True)
            # Pole vector
            # pole_pos = self.get_pole_position(fk_ctrl_start, fk_ctrl_mid, fk_ctrl_end, 2)
            # cmds.move(pole_pos[0], pole_pos[1], pole_pos[2], ik_pole_ctrl, absolute=True, worldSpace=True)
            pole_locator = self.create_loc(fk_ctrl_start, fk_ctrl_mid, fk_ctrl_end, 2)
            cmds.matchTransform(ik_pole_ctrl, pole_locator)
            cmds.delete(pole_locator)

        elif ikfk_attr_value == int(settings_dict.get("IK")):
            # Set attribute
            cmds.setAttr(ikfk_attr_name, 1)

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
        self.output_file_path = cmds.internalVar(userPrefDir=True)+"ikfk_settings_{}.json".format(limb_name)
        self.setWindowTitle("Settings - "+limb_name)
        self.setWindowIcon(QtGui.QIcon(":advancedSettings.png"))
        
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.resize(320, 120)
        self.create_ui_layout()
        self.create_ui_connections()

        if cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)
            
    def create_ui_layout(self):
        settings_dict = {}
        try:
            settings_dict = json.load(open(self.output_file_path))
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
        main_layout.setContentsMargins(10, 20, 10, 10)

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
        
        self.textfield_widget_dict.get("IK").setFixedWidth(24)
        self.textfield_widget_dict.get("FK").setFixedWidth(24)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
 
    def create_ui_connections(self):
        self.save_button.clicked.connect(self.save_settings)
        self.close_button.clicked.connect(self.close_settings)

    def close_settings(self):
        self.close()
        self.deleteLater()

    def save_settings(self):
        try:
            for key, value in self.textfield_widget_dict.iteritems():
                self.output_data_dict[key] = value.text()

            with open(self.output_file_path, "w") as outfile:
                json.dump(self.output_data_dict, outfile, indent=4)
            print("Saved settings: "+self.output_file_path)
            self.close()
            self.deleteLater()
        except:
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