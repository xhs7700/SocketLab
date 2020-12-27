# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.MainGridLayout = QGridLayout()
        self.MainGridLayout.setObjectName(u"MainGridLayout")

        self.horizontalLayout.addLayout(self.MainGridLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.MainStatusBar = QStatusBar(MainWindow)
        self.MainStatusBar.setObjectName(u"MainStatusBar")
        MainWindow.setStatusBar(self.MainStatusBar)
        self.MainToolBar = QToolBar(MainWindow)
        self.MainToolBar.setObjectName(u"MainToolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.MainToolBar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.MainToolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi
