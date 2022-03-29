'''
Name: search_replace_names
Description: A tool for searching and replacing a string in the name of the selected nodes.
 
Author: Joar Engberg 2022
'''

import re
import sys
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from functools import partial
from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance


def maya_main_window():
    # Return the Maya main window as QMainWindow
    main_window = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window), QtWidgets.QWidget) # type: ignore


class SearchReplaceTool(QtWidgets.QDialog):

    def __init__(self):
        super(SearchReplaceTool, self).__init__(maya_main_window())

        self.script_job_ids = []
        self.renamed_nodes = []
        self.cached_selected = []

        self.setWindowTitle("Search and replace string")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.resize(300, 300)
        self.create_ui_widgets()
        self.create_ui_layout()
        self.create_ui_connections()
        self.create_script_job()
 
    def create_ui_widgets(self):
        self.apply_button = QtWidgets.QPushButton("Apply")
        self.close_button = QtWidgets.QPushButton("Close")
        self.find_line = QtWidgets.QLineEdit()
        self.replace_line = QtWidgets.QLineEdit()
        self.string_line = QtWidgets.QTextEdit()
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
        selected = cmds.ls(selection=True)
        self.string_line.clear()

        try:
            for i in range(len(selected)):
                # self.string_line.append(selected[i])

                if selected[i] != self.cached_selected[i]:
                    self.string_line.setTextColor("#39FF14")
                    self.string_line.append(selected[i])
                else:
                    self.string_line.setTextColor("#FFFFFF")
                    self.string_line.append(selected[i])
        except:
            self.string_line.setTextColor("#FF0000")
            self.string_line.setText("Error! Could not rename nodes.")
        
        self.string_line.setTextColor("#FFFFFF")


    def on_selection_changed(self):
        selected = cmds.ls(selection=True)
        self.string_line.clear()
        self.string_line.setTextColor("#FFFFFF")
        for sel in selected:
            self.string_line.append(sel)

    def closeEvent(self, event):
        self.kill_script_job()

    def close_window(self):
        self.kill_script_job()
        try:
            search_replace_ui.close() # type: ignore
            search_replace_ui.deleteLater() # type: ignore
        except:
            pass

    def rename_node(self):
        selected = cmds.ls(selection=True, objectsOnly=True)
        self.cached_selected = selected
        find = self.find_line.text()
        replace_with = self.replace_line.text()
        self.renamed_nodes = []

        if self.case_checkbox.isChecked() == True:
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
    search_replace_ui = SearchReplaceTool()
    search_replace_ui.show()

if __name__ == "__main__":
    start()
