# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from graph import GraphicsWidget
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1663, 855)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.centralwidget_2.setGeometry(QtCore.QRect(0, 0, 2021, 821))
        self.centralwidget_2.setObjectName("centralwidget_2")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget_2)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1281, 781))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphics_widget = GraphicsWidget(self.horizontalLayoutWidget)
        self.graphics_widget.setObjectName("graphics_widget")
        self.horizontalLayout.addWidget(self.graphics_widget)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget_2)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(1310, 10, 341, 551))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(self.horizontalLayoutWidget_2)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.apply_local_transition = QtWidgets.QPushButton(self.frame)
        self.apply_local_transition.setGeometry(QtCore.QRect(30, 80, 281, 31))
        self.apply_local_transition.setObjectName("apply_local_transition")
        self.input_local_transition_x = QtWidgets.QLineEdit(self.frame)
        self.input_local_transition_x.setGeometry(QtCore.QRect(50, 50, 113, 25))
        self.input_local_transition_x.setObjectName("input_local_transition_x")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(30, 50, 21, 17))
        self.label_2.setObjectName("label_2")
        self.input_local_transition_y = QtWidgets.QLineEdit(self.frame)
        self.input_local_transition_y.setGeometry(QtCore.QRect(200, 50, 113, 25))
        self.input_local_transition_y.setObjectName("input_local_transition_y")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(80, 20, 201, 20))
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(180, 50, 21, 17))
        self.label.setObjectName("label")
        self.apply_rotation = QtWidgets.QPushButton(self.frame)
        self.apply_rotation.setGeometry(QtCore.QRect(30, 220, 281, 31))
        self.apply_rotation.setObjectName("apply_rotation")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setGeometry(QtCore.QRect(60, 130, 211, 20))
        self.label_7.setObjectName("label_7")
        self.input_rotation_x = QtWidgets.QLineEdit(self.frame)
        self.input_rotation_x.setGeometry(QtCore.QRect(50, 190, 113, 25))
        self.input_rotation_x.setObjectName("input_rotation_x")
        self.label_10 = QtWidgets.QLabel(self.frame)
        self.label_10.setGeometry(QtCore.QRect(80, 160, 61, 20))
        self.label_10.setObjectName("label_10")
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setGeometry(QtCore.QRect(30, 190, 21, 17))
        self.label_8.setObjectName("label_8")
        self.input_rotation_angle = QtWidgets.QLineEdit(self.frame)
        self.input_rotation_angle.setGeometry(QtCore.QRect(130, 160, 113, 25))
        self.input_rotation_angle.setObjectName("input_rotation_angle")
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setGeometry(QtCore.QRect(180, 190, 21, 17))
        self.label_9.setObjectName("label_9")
        self.input_rotation_y = QtWidgets.QLineEdit(self.frame)
        self.input_rotation_y.setGeometry(QtCore.QRect(200, 190, 113, 25))
        self.input_rotation_y.setObjectName("input_rotation_y")
        self.apply_scale = QtWidgets.QPushButton(self.frame)
        self.apply_scale.setGeometry(QtCore.QRect(30, 370, 281, 31))
        self.apply_scale.setObjectName("apply_scale")
        self.label_15 = QtWidgets.QLabel(self.frame)
        self.label_15.setGeometry(QtCore.QRect(170, 310, 21, 17))
        self.label_15.setObjectName("label_15")
        self.label_14 = QtWidgets.QLabel(self.frame)
        self.label_14.setGeometry(QtCore.QRect(180, 340, 21, 17))
        self.label_14.setObjectName("label_14")
        self.input_scale_x = QtWidgets.QLineEdit(self.frame)
        self.input_scale_x.setGeometry(QtCore.QRect(50, 340, 113, 25))
        self.input_scale_x.setObjectName("input_scale_x")
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setGeometry(QtCore.QRect(10, 280, 281, 20))
        self.label_11.setObjectName("label_11")
        self.input_scale_kx = QtWidgets.QLineEdit(self.frame)
        self.input_scale_kx.setGeometry(QtCore.QRect(50, 310, 113, 25))
        self.input_scale_kx.setObjectName("input_scale_kx")
        self.input_scale_ky = QtWidgets.QLineEdit(self.frame)
        self.input_scale_ky.setGeometry(QtCore.QRect(200, 310, 113, 25))
        self.input_scale_ky.setObjectName("input_scale_ky")
        self.input_scale_y = QtWidgets.QLineEdit(self.frame)
        self.input_scale_y.setGeometry(QtCore.QRect(200, 340, 113, 25))
        self.input_scale_y.setObjectName("input_scale_y")
        self.label_13 = QtWidgets.QLabel(self.frame)
        self.label_13.setGeometry(QtCore.QRect(20, 310, 21, 17))
        self.label_13.setObjectName("label_13")
        self.label_12 = QtWidgets.QLabel(self.frame)
        self.label_12.setGeometry(QtCore.QRect(30, 340, 21, 17))
        self.label_12.setObjectName("label_12")
        self.apply_undo = QtWidgets.QPushButton(self.frame)
        self.apply_undo.setGeometry(QtCore.QRect(40, 450, 121, 31))
        self.apply_undo.setObjectName("apply_undo")
        self.transition_info = QtWidgets.QPushButton(self.frame)
        self.transition_info.setGeometry(QtCore.QRect(300, 20, 31, 25))
        self.transition_info.setObjectName("transition_info")
        self.apply_redo = QtWidgets.QPushButton(self.frame)
        self.apply_redo.setGeometry(QtCore.QRect(180, 450, 121, 31))
        self.apply_redo.setObjectName("apply_redo")
        self.init_figure = QtWidgets.QPushButton(self.frame)
        self.init_figure.setGeometry(QtCore.QRect(170, 500, 121, 31))
        self.init_figure.setObjectName("init_figure")
        self.rotation_info = QtWidgets.QPushButton(self.frame)
        self.rotation_info.setGeometry(QtCore.QRect(300, 130, 31, 25))
        self.rotation_info.setObjectName("rotation_info")
        self.scale_info = QtWidgets.QPushButton(self.frame)
        self.scale_info.setGeometry(QtCore.QRect(300, 280, 31, 25))
        self.scale_info.setObjectName("scale_info")
        self.input_radius = QtWidgets.QLineEdit(self.frame)
        self.input_radius.setGeometry(QtCore.QRect(100, 500, 61, 25))
        self.input_radius.setObjectName("input_radius")
        self.label_37 = QtWidgets.QLabel(self.frame)
        self.label_37.setGeometry(QtCore.QRect(40, 500, 61, 20))
        self.label_37.setObjectName("label_37")
        self.reset_info = QtWidgets.QPushButton(self.frame)
        self.reset_info.setGeometry(QtCore.QRect(300, 500, 31, 25))
        self.reset_info.setObjectName("reset_info")
        self.horizontalLayout_2.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1663, 22))
        self.menubar.setObjectName("menubar")
        self.menuinfo = QtWidgets.QMenu(self.menubar)
        self.menuinfo.setObjectName("menuinfo")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.menuinfo.addAction(self.action)
        self.menubar.addAction(self.menuinfo.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.apply_local_transition.setText(_translate("MainWindow", "Применить смещение"))
        self.label_2.setText(_translate("MainWindow", "X:"))
        self.label_3.setText(_translate("MainWindow", "Относительное смещение"))
        self.label.setText(_translate("MainWindow", "Y:"))
        self.apply_rotation.setText(_translate("MainWindow", "Применить поворот"))
        self.label_7.setText(_translate("MainWindow", "Поворот относительно точки"))
        self.label_10.setText(_translate("MainWindow", "Угол:"))
        self.label_8.setText(_translate("MainWindow", "X:"))
        self.label_9.setText(_translate("MainWindow", "Y:"))
        self.apply_scale.setText(_translate("MainWindow", "Применить масштабирование"))
        self.label_15.setText(_translate("MainWindow", "kY:"))
        self.label_14.setText(_translate("MainWindow", "Y:"))
        self.label_11.setText(_translate("MainWindow", "Масштабирование относительно точки"))
        self.label_13.setText(_translate("MainWindow", "kX:"))
        self.label_12.setText(_translate("MainWindow", "X:"))
        self.apply_undo.setText(_translate("MainWindow", "Назад"))
        self.transition_info.setText(_translate("MainWindow", "?"))
        self.apply_redo.setText(_translate("MainWindow", "Вперёд"))
        self.init_figure.setText(_translate("MainWindow", "Сбросить"))
        self.rotation_info.setText(_translate("MainWindow", "?"))
        self.scale_info.setText(_translate("MainWindow", "?"))
        self.input_radius.setText(_translate("MainWindow", "100"))
        self.label_37.setText(_translate("MainWindow", "Радиус:"))
        self.reset_info.setText(_translate("MainWindow", "?"))
        self.menuinfo.setTitle(_translate("MainWindow", "Справка"))
        self.action.setText(_translate("MainWindow", "О программе"))
