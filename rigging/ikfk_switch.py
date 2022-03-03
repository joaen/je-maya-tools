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
        self.setWindowTitle("IK/FK Switch")
        
        # self.output_file_path = cmds.internalVar(userPrefDir=True)+"{}_settings.json".format(limb_name)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.resize(360, 120)
        self.create_ui_widgets()
        self.create_ui_layout()
        self.create_ui_connections()

        if cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)
 
    def create_ui_widgets(self):
        self.template_label = QtWidgets.QLabel("Switch IK/FK:")

        self.template_button1 = QtWidgets.QPushButton("RIGHT ARM")
        self.template_button1.setStyleSheet("background-color: lightgreen; color: black")
        self.template_button2 = QtWidgets.QPushButton("LEFT ARM")
        self.template_button2.setStyleSheet("background-color: salmon; color: black")
        self.template_button3 = QtWidgets.QPushButton("RIGHT LEG")
        self.template_button3.setStyleSheet("background-color: lightgreen; color: black")
        self.template_button4 = QtWidgets.QPushButton("LEFT LEG")
        self.template_button4.setStyleSheet("background-color: salmon; color: black")

        self.template_checkbox = QtWidgets.QCheckBox("TEMPLATE_CHECKBOX")
        self.template_combobox = QtWidgets.QComboBox()
        self.template_combobox.addItem("TEMPLATE_COMBOBOX_ITEM")
        self.template_textfield = QtWidgets.QLineEdit()
        self.template_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)

        self.close_button = QtWidgets.QPushButton("Close")
        self.close_button.setFixedWidth(100)

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
        # horizontal_layout.addWidget(self.settings1_button)
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(self.help_icon_button)
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

        self.template_button1.clicked.connect(partial(self.switch, "RightArm"))
        self.template_button2.clicked.connect(partial(self.switch, "LeftArm"))
        self.template_button3.clicked.connect(partial(self.switch, "RightLeg"))
        self.template_button4.clicked.connect(partial(self.switch, "LeftLeg"))
        self.close_button.clicked.connect(self.close_ikfk_window)

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
    
    def switch(self, limb_name):
        self.output_file_path = cmds.internalVar(userPrefDir=True)+"ikfk_settings_{}.json".format(limb_name)
        settings_dict = json.load(open(self.output_file_path))
        # Attritbute
        ikfk_attr_name = settings_dict.get("ikfk_attr_name")
        print("Loaded settings from: "+self.output_file_path)
        # print(ikfk_attr_name)

        ikfk_attr_value = cmds.getAttr(ikfk_attr_name)

        # # FK

        fk_ctrl_start = settings_dict.get("fk_ctrl_start")
        fk_ctrl_mid = settings_dict.get("fk_ctrl_mid")
        fk_ctrl_end = settings_dict.get("fk_ctrl_end")
        
        ik_joint_start = settings_dict.get("ik_joint_start")
        ik_joint_mid = settings_dict.get("ik_joint_mid")
        ik_joint_end = settings_dict.get("ik_joint_end")

        # IK 
        ik_ctrl = settings_dict.get("ik_ctrl")
        ik_pv_ctrl = settings_dict.get("ik_pv_ctrl")

        fk_joint_start = settings_dict.get("fk_joint_start")
        fk_joint_mid = settings_dict.get("fk_joint_mid")
        fk_joint_end = settings_dict.get("fk_joint_end")

        if ikfk_attr_value == 1:
            # Set attribute
            cmds.setAttr(ikfk_attr_name, 0)

            # IK controller
            pos = om.MVector(cmds.xform(fk_joint_end, query=True, translation=True, worldSpace=True))
            mat = om.MMatrix(cmds.xform(fk_joint_end, query=True, matrix=True, worldSpace=True))
            
            side_vector = om.MVector(mat[0], mat[1], mat[2])
            up_vector = om.MVector(mat[4], mat[5], mat[6])
            fwd_vector = om.MVector(mat[8], mat[9], mat[10])

            x = [side_vector.x, side_vector.y, side_vector.z, 0]
            y = [up_vector.x, up_vector.y, up_vector.z, 0]
            z = [fwd_vector.x, fwd_vector.y, fwd_vector.z, 0]
            o = [pos.x, pos.y, pos.z, 1]

            matrix_list = [x, y, z, o]
            joint_matrix = om.MMatrix(matrix_list)
            cmds.xform(ik_ctrl, matrix=joint_matrix, worldSpace=True)

            # Pole vector
            cmds.matchTransform(ik_pv_ctrl, fk_joint_mid, position=True)

        elif ikfk_attr_value == 0:
            # Set attribute
            cmds.setAttr(ikfk_attr_name, 1)

            cmds.matchTransform(fk_ctrl_start, ik_joint_start, rotation=True)
            cmds.matchTransform(fk_ctrl_mid, ik_joint_mid, rotation=True)
            cmds.matchTransform(fk_ctrl_end, ik_joint_end, rotation=True)


class SettingsWindow(QtWidgets.QDialog):

    textfield_widget_dict = {
        "ikfk_attr_name" : "",
        "fk_ctrl_start" : "",
        "fk_ctrl_mid" : "",
        "fk_ctrl_end" : "",
        "ik_joint_start" : "",
        "ik_joint_mid" : "",
        "ik_joint_end" : "",
        "ik_ctrl" : "",
        "ik_pv_ctrl" : "",
        "fk_joint_start" : "",
        "fk_joint_mid" : "",
        "fk_joint_end" : ""
    }

    output_data_dict = {
        "ikfk_attr_name" : "",
        "fk_ctrl_start" : "",
        "fk_ctrl_mid" : "",
        "fk_ctrl_end" : "",
        "ik_joint_start" : "",
        "ik_joint_mid" : "",
        "ik_joint_end" : "",
        "ik_ctrl" : "",
        "ik_pv_ctrl" : "",
        "fk_joint_start" : "",
        "fk_joint_mid" : "",
        "fk_joint_end" : ""
    }


    def __init__(self, limb_name):
        super(SettingsWindow, self).__init__(maya_main_window())
        self.output_file_path = cmds.internalVar(userPrefDir=True)+"ikfk_settings_{}.json".format(limb_name)
        self.setWindowTitle("Settings - "+limb_name)
        self.setWindowIcon(QtGui.QIcon(":advancedSettings.png"))
        
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.resize(320, 120)
        self.create_ui()
        self.create_ui_connections()

        if cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)
            
    def create_ui(self):
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

        for key in self.textfield_widget_dict:
            label = QtWidgets.QLabel(str(key))
            label_layout = QtWidgets.QHBoxLayout()
            label_layout.addWidget(label)
            label_layout.addWidget(self.textfield_widget_dict[key])
            main_layout.addLayout(label_layout)
        
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