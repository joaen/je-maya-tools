from distutils.command import check
from functools import partial
import sys

import maya.api.OpenMaya as om2
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance
import re


def maya_main_window():
    # Return the Maya main window as QMainWindow
    main_window = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window), QtWidgets.QWidget) # type: ignore


class RenameTool(QtWidgets.QDialog):

    def __init__(self):
        super(RenameTool, self).__init__(maya_main_window())

        self.script_job_ids = []
        self.renamed_nodes = []
        self.setWindowTitle("Search and replace string")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.resize(300, 100)
        self.create_ui_widgets()
        self.create_ui_layout()
        self.create_ui_connections()
        self.create_script_job()
 
    def create_ui_widgets(self):
        self.apply_button = QtWidgets.QPushButton("Apply")
        self.close_button = QtWidgets.QPushButton("Close")
        self.find_line = QtWidgets.QLineEdit()
        self.replace_line = QtWidgets.QLineEdit()
        self.string_line = QtWidgets.QLineEdit()
        self.case_checkbox = QtWidgets.QCheckBox()
        self.case_checkbox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.case_checkbox.setText("Ignore case:")
        self.case_checkbox.setChecked(0)
        self.string_line.setStyleSheet("background-color: #3A3A3A; color: #000000;")
        self.string_line.setDisabled(1)

    def create_ui_layout(self):
        upper_row = QtWidgets.QFormLayout()
        upper_row.addRow("Find:", self.find_line)
        upper_row.addRow("Replace:", self.replace_line)
        upper_row.addRow("Selection:", self.string_line)

        lower_row = QtWidgets.QHBoxLayout()
        lower_row.addWidget(self.case_checkbox)
        lower_row.addWidget(self.apply_button)
        lower_row.addWidget(self.close_button)
        lower_row.setAlignment(QtCore.Qt.AlignBottom)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addLayout(upper_row)
        main_layout.addLayout(lower_row)
 
    def create_ui_connections(self):
        self.apply_button.clicked.connect(self.rename_node)
        self.close_button.clicked.connect(self.close_window)

    def create_script_job(self):
        self.script_job_ids.append(cmds.scriptJob(event=["SelectionChanged", partial(self.on_selection_changed)]))
        self.script_job_ids.append(cmds.scriptJob(event=["NameChanged", partial(self.on_name_changed)]))

    def kill_script_job(self):
        for id in self.script_job_ids:
            if cmds.scriptJob(exists=id):
                cmds.scriptJob(kill=id)
            else:
                pass

    def on_name_changed(self):
        selected = cmds.ls(sl=True)
        selected_count = len(selected)
        try:
            if selected_count == 1:
                self.string_line.setText(selected[0])
                self.string_line.setStyleSheet("background-color: #3A3A3A; color: #39FF14;")
            if selected_count > 1:
                self.string_line.setText("Successfully renamed {} objects!".format(len(self.renamed_nodes)))
                self.string_line.setStyleSheet("background-color: #3A3A3A; color: #39FF14;")
        except:
            self.string_line.setStyleSheet("background-color: #FF0000; color: #000000")
            self.string_line.setText("Error! Could not rename nodes.")

    def on_selection_changed(self):
        selected = cmds.ls(sl=True)
        selected_count = len(selected)
        if selected_count == 1:
            self.string_line.setText(selected[0])
            self.string_line.setStyleSheet("background-color: #3A3A3A; color: #00FFFF;")
        if selected_count > 1:
            self.string_line.setText("Number of selected nodes: {}".format(selected_count))
            self.string_line.setStyleSheet("background-color: #3A3A3A; color: #00FFFF;")
        elif selected_count < 1:
            self.string_line.setStyleSheet("background-color: #3A3A3A;")
            self.string_line.setText("")

    def get_find_string(self):
        find_string = self.find_line.text()
        return find_string
    
    def get_replace_string(self):
        replace_string = self.replace_line.text()
        return replace_string

    def closeEvent(self, event):
        self.kill_script_job()

    def close_window(self):
        self.kill_script_job()
        try:
            search_replace_ui.close() # type: ignore
            search_replace_ui.deleteLater() # type: ignore
        except:
            pass

    def get_case_checkbox(self):
        checkbox_value = self.case_checkbox.isChecked()
        return checkbox_value

    def rename_node(self):
        selected = cmds.ls(sl=True, objectsOnly=True)
        find = self.get_find_string()
        replace_with = self.get_replace_string()
        self.renamed_nodes = []

        if self.get_case_checkbox() == True:
            for name in selected:
                if find.lower() in name.lower():
                    # String replace doesn't have a ignore case flag so using re.sub instead
                    new_name = re.sub(find, replace_with, name, flags=re.IGNORECASE)
                    cmds.rename(name, new_name)
                    self.renamed_nodes.append(name)
        else:
            for name in selected:
                if find in name:
                    new_name = name.replace(find, replace_with)
                    cmds.rename(name, new_name)
                    self.renamed_nodes.append(name)

def start():
    global search_replace_ui
    try:
        search_replace_ui.close() # type: ignore
        search_replace_ui.deleteLater() # type: ignore
    except:
        pass
    search_replace_ui = RenameTool()
    search_replace_ui.show()

if __name__ == "__main__":
    start()
