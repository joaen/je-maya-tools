import sys
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtCore, QtGui, QtWidgets
import json


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
        
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.resize(320, 120)
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
        
        self.template_icon_button = QtWidgets.QPushButton()
        self.template_icon_button.setIcon(QtGui.QIcon(":advancedSettings.png"))
        self.template_icon_button.setFixedSize(24, 24)
        self.template_icon_button.setStyleSheet(icon_button_css)

        self.help_icon_button = QtWidgets.QPushButton()
        self.help_icon_button.setIcon(QtGui.QIcon(":help.png"))
        self.help_icon_button.setFixedSize(24, 24)
        self.help_icon_button.setStyleSheet(icon_button_css)

        

    def create_ui_layout(self):

        horizontal_layout1 = QtWidgets.QHBoxLayout()
        horizontal_layout1.addWidget(self.template_button1)
        horizontal_layout1.addWidget(self.template_button2)

        horizontal_layout2 = QtWidgets.QHBoxLayout()
        horizontal_layout2.addWidget(self.template_button3)
        horizontal_layout2.addWidget(self.template_button4)
        # vertical_layout.addWidget(self.template_label)
        # vertical_layout.addWidget(self.template_checkbox)
        # vertical_layout.addWidget(self.template_combobox)
        # vertical_layout.addWidget(self.template_slider)
        # horizontal_layout2.addSpacing(20)

        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addWidget(self.template_icon_button)
        horizontal_layout.addWidget(self.help_icon_button)
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(self.close_button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)
        # main_layout.addWidget(self.template_label)
        # main_layout
        main_layout.addLayout(horizontal_layout1)
        main_layout.addLayout(horizontal_layout2)
        main_layout.addSpacing(30)
        main_layout.addLayout(horizontal_layout)
        main_layout.addStretch()
        # main_layout.addLayout(vertical_layout)
 
    def create_ui_connections(self):
        # self.template_button1.clicked.connect(self.open_settings_window)
        self.template_icon_button.clicked.connect(self.open_settings_window)
        # self.template_slider.valueChanged.connect(self.open_settings_window)

    def open_settings_window(self):
        try:
            self.settings_window.close()
            self.settings_window.deleteLater()
        except:
            pass
        self.settings_window = SettingsWindow()
        self.settings_window.show()


class SettingsWindow(QtWidgets.QDialog):

    # textfield_label_list = [
    #     "ikfk_attr_name", "fk_ctrl_start", "fk_ctrl_mid", "fk_ctrl_end",
    #     "ik_target_start", "ik_target_mid", "ik_target_end", "ik_ctrl",
    #     "ik_pv_ctrl", "fk_target_start", "fk_target_mid", "fk_target_end"
    # ]

    textfield_widget_dict = {
        "ikfk_attr_name" : "",
        "fk_ctrl_start" : "",
        "fk_ctrl_mid" : "",
        "fk_ctrl_end" : "",
        "ik_target_start" : "",
        "ik_target_mid" : "",
        "ik_target_end" : "",
        "ik_ctrl" : "",
        "ik_pv_ctrl" : "",
        "fk_target_start" : "",
        "fk_target_mid" : "",
        "fk_target_end" : ""
    }

    output_data_dict = {
        "ikfk_attr_name" : "",
        "fk_ctrl_start" : "",
        "fk_ctrl_mid" : "",
        "fk_ctrl_end" : "",
        "ik_target_start" : "",
        "ik_target_mid" : "",
        "ik_target_end" : "",
        "ik_ctrl" : "",
        "ik_pv_ctrl" : "",
        "fk_target_start" : "",
        "fk_target_mid" : "",
        "fk_target_end" : ""
    }

    output_path = cmds.internalVar(userPrefDir=True)+"ikfk_switch_settings.json"

    def __init__(self):
        super(SettingsWindow, self).__init__(maya_main_window())
        self.setWindowTitle("Settings")
        self.setWindowIcon(QtGui.QIcon(":advancedSettings.png"))
        
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.resize(320, 120)
        self.create_ui()
        self.create_ui_connections()

        if cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)
            
    def create_ui(self):
        # self.label_widget_list = []
        settings_dict = json.load(open(self.output_path))

        for key in self.textfield_widget_dict:
            label = QtWidgets.QLabel(str(key))
            textfield = QtWidgets.QLineEdit()
            # textfield.text
            # self.label_widget_list.append(label)
            textfield.setText(settings_dict[key])
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
            # label.setTe
        
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
 
    def create_ui_connections(self):
        self.save_button.clicked.connect(self.save_settings)
        self.close_button.clicked.connect(self.close_settings)

    def close_settings(self):
        print(self.label_widget_list[0])


    def save_settings(self):
        for key, value in self.textfield_widget_dict.iteritems():
            # self.textfield_widget_dict.get(key) = 
            self.output_data_dict[key] = value.text()
            print(value.text())

        # with open(self.output_path, 'w') as outfile:
        #     json.dump(self.output_data_dict, outfile, indent=4)

        print("Saved settings: "+self.output_path)

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