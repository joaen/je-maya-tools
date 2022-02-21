import sys
import pymel.core as pm
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtCore, QtGui, QtWidgets


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
        self.setWindowTitle("Ctrl Creator")
        
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.resize(380, 250)
        self.create_ui_widgets()
        self.create_ui_layout()
        self.create_ui_connections()

        if pm.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)
 
    def create_ui_widgets(self):
        self.template_label = QtWidgets.QLabel("Create controllers")
        self.template_label.setStyleSheet("background-color: #5d5d5d; border: 1px solid #5d5d5d; border-radius: 2px;font-weight: bold;")
        self.template_label.setFixedHeight(20)

        self.template_label_e = QtWidgets.QLabel("Edit controllers")
        self.template_label_e.setStyleSheet("background-color: #5d5d5d; border: 1px solid #5d5d5d; border-radius: 2px;font-weight: bold;")
        self.template_label_e.setFixedHeight(20)

        self.template_button = QtWidgets.QPushButton("TEMPLATE BUTTON")
        self.template_combobox = QtWidgets.QComboBox()
        self.template_combobox.addItem("TEMPLATE_COMBOBOX_ITEM")
        self.template_textfield = QtWidgets.QLineEdit()
        self.template_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.template_icon1_button = QtWidgets.QPushButton(QtGui.QIcon(":circle.png"), "Circle")
        self.template_icon2_button = QtWidgets.QPushButton(QtGui.QIcon(":sphere.png"), "Sphere")
        self.template_icon3_button = QtWidgets.QPushButton(QtGui.QIcon(":square.png"), "Square")
        self.template_icon4_button = QtWidgets.QPushButton(QtGui.QIcon(":cube.png"), "Cube")
        
        self.template_checkbox1 = QtWidgets.QCheckBox("ParentConstraint")
        self.template_checkbox2 = QtWidgets.QCheckBox("Hide + lock unused attrs")
        self.template_checkbox3 = QtWidgets.QCheckBox("_FK suffix")

        self.template_label1 = QtWidgets.QLabel("Scale:")
        self.template_btn1 = QtWidgets.QPushButton("+")
        self.template_btn1.setFixedWidth(30)
        self.template_btn2 = QtWidgets.QPushButton("-")
        self.template_btn2.setFixedWidth(30)
        self.template_label2 = QtWidgets.QLabel("Rotate:")
        self.template_btn3 = QtWidgets.QPushButton("X")
        self.template_btn3.setFixedWidth(30)
        self.template_btn4 = QtWidgets.QPushButton("Y")
        self.template_btn4.setFixedWidth(30)
        self.template_btn5 = QtWidgets.QPushButton("Z")
        self.template_btn5.setFixedWidth(30)

        self.template_button1 = QtWidgets.QPushButton(QtGui.QIcon(":noAccess.png"), "")
        self.template_button1.setFixedHeight(25)
        self.template_button1.setStyleSheet("background-color: grey")
        self.template_button2 = QtWidgets.QPushButton()
        self.template_button2.setStyleSheet("background-color: blue")
        self.template_button3 = QtWidgets.QPushButton()
        self.template_button3.setStyleSheet("background-color: darkblue")
        self.template_button4 = QtWidgets.QPushButton()
        self.template_button4.setStyleSheet("background-color: purple")
        self.template_button5 = QtWidgets.QPushButton()
        self.template_button5.setStyleSheet("background-color: magenta")
        self.template_button6 = QtWidgets.QPushButton()
        self.template_button6.setStyleSheet("background-color: red")
        self.template_button7 = QtWidgets.QPushButton()
        self.template_button7.setStyleSheet("background-color: darkred")
        self.template_button8 = QtWidgets.QPushButton()
        self.template_button8.setStyleSheet("background-color: yellow")
        self.template_button9 = QtWidgets.QPushButton()
        self.template_button9.setStyleSheet("background-color: #00FF00")
        self.template_button10 = QtWidgets.QPushButton()
        self.template_button10.setStyleSheet("background-color: white")

        # self.template_border = QtWidgets.QFrame()
        # self.template_border.setFrameShape(QtWidgets.QFrame.HLine)
        # self.template_border.setFixedHeight(100)


    def create_ui_layout(self):
        horizontal_layout2 = QtWidgets.QHBoxLayout()
        # horizontal_layout2.addWidget(self.template_border)
        # horizontal_layout2.addWidget(self.template_label)
        horizontal_layout2.setContentsMargins(0,0,0,20)
        horizontal_layout2.addWidget(self.template_checkbox1)
        horizontal_layout2.addWidget(self.template_checkbox2)
        horizontal_layout2.addWidget(self.template_checkbox3)

        horizontal_layout = QtWidgets.QHBoxLayout()
        # horizontal_layout.setContentsMargins(0, 0, 0, 40)
        horizontal_layout.addWidget(self.template_icon1_button)
        horizontal_layout.addWidget(self.template_icon2_button)
        horizontal_layout.addWidget(self.template_icon3_button)
        horizontal_layout.addWidget(self.template_icon4_button)
        # horizontal_layout.addStretch(QtCore.Qt.Horizontal)

        edit_layout = QtWidgets.QHBoxLayout()
        edit_layout.addWidget(self.template_label2)
        edit_layout.addWidget(self.template_btn3)
        edit_layout.addWidget(self.template_btn4)
        edit_layout.addWidget(self.template_btn5)
        edit_layout.addWidget(self.template_label1)
        edit_layout.addWidget(self.template_btn1)
        edit_layout.addWidget(self.template_btn2)
        # vertical_layout.addWidget(self.template_la
        # ebel)
        # vertical_layout.addWidget(self.template_checkbox)
        # vertical_layout.addWidget(self.template_combobox)
        # vertical_layout.addWidget(self.template_slider)
        # vertical_layout.addStretch()
        color_upper_row = QtWidgets.QHBoxLayout()
        color_upper_row.setSpacing(0)
        color_upper_row.addWidget(self.template_button1)
        color_upper_row.addWidget(self.template_button2)
        color_upper_row.addWidget(self.template_button3)
        color_upper_row.addWidget(self.template_button4)
        color_upper_row.addWidget(self.template_button5)
        color_upper_row.addWidget(self.template_button6)
        color_upper_row.addWidget(self.template_button7)
        color_upper_row.addWidget(self.template_button8)
        color_upper_row.addWidget(self.template_button9)
        color_upper_row.addWidget(self.template_button10)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(self.template_label)
        main_layout.addLayout(horizontal_layout)
        main_layout.addLayout(horizontal_layout2)
        main_layout.addWidget(self.template_label_e)
        main_layout.addLayout(edit_layout)
        main_layout.addLayout(color_upper_row)
        main_layout.addStretch()
        # main_layout.addLayout(vertical_layout)
 
    def create_ui_connections(self):
        # self.template_button.clicked.connect(self.template_command)
        self.template_icon1_button.clicked.connect(self.template_command)
        # self.template_slider.valueChanged.connect(self.template_command)

    def template_command(self):
        print("WOW")
        # color = QtWidgets.QColorDialog.getColor()
    
    def get_cvs(self, object):
        spans = str(pm.getAttr(object+".spans") - 1)
        ctrl_vertices = "{shape}.cv[0:{count}]".format(shape=object, count=spans)
        return ctrl_vertices

    def create_controller(self):
        for transform in pm.selected():
            shape = self.create_sphere()
            pm.rename(shape, transform+"_CTRL")
            offset_grp = pm.group(shape)
            pm.rename(offset_grp, transform+"_CTRL_Grp")
            pm.matchTransform(offset_grp, transform)

    def scale_ctrl_shape(self, size):
        stored_selection = pm.ls(selection=True)

        for ctrl in pm.selected():
            pm.select(self.get_cvs(ctrl), replace=True)
            pm.scale(size, size, size)
        
        pm.select(clear=True)
        for sel in stored_selection:
            pm.select(sel, add=True)

    def rotate_ctrl_shape(self, degrees):
        stored_selection = pm.ls(selection=True)

        for ctrl in pm.selected(self):
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
        
        # Combine
        shape_nodes = pm.listRelatives(circles, shapes=True)
        output_node = pm.group(empty=True)
        pm.makeIdentity(circles, apply=True, t=True, r=True, s=True)
        pm.parent(shape_nodes, output_node, shape=True, relative=True)
        pm.delete(shape_nodes, constructionHistory=True)
        pm.delete(circles)
        return output_node

    def create_circle(self):
        return pm.circle(normal=(1, 0, 0), center=(0, 0, 0))

    def create_cube(self):
        return pm.curve(name="shape123", d=1, p=[(-1, -1, 1), (-1, 1, 1), (1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, -1, -1), (-1, 1, -1), (-1, 1, 1), (-1, 1, -1), (1, 1, -1), (1, -1, -1), (-1, -1, -1), (1, -1, -1), (1, -1, 1), (1, 1, 1), (1, 1, -1)], k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

    def create_square(self):
        return pm.curve(d=1, p=[(-1, 0, 1), (-1, 0, 1), (0, 0, 1), (1, 0, 1), (1, 0, 1), (1, 0, -1), (-1, 0, -1), (-1, 0, 1)], k=[0,1,2,3,4,5,6,7])

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