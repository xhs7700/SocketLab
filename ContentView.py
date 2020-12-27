# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ContentView.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 600)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.MarkdownText)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.ChapterLabel = QLabel(Form)
        self.ChapterLabel.setObjectName(u"ChapterLabel")
        self.ChapterLabel.setTextFormat(Qt.MarkdownText)

        self.verticalLayout.addWidget(self.ChapterLabel)

        self.ContentTextEdit = QPlainTextEdit(Form)
        self.ContentTextEdit.setObjectName(u"ContentTextEdit")
        self.ContentTextEdit.setFont(font)
        self.ContentTextEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.ContentTextEdit)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"# Simple Reader -- Content", None))
        self.ChapterLabel.setText(QCoreApplication.translate("Form", u"## ", None))
        self.ContentTextEdit.setPlainText("")
    # retranslateUi
