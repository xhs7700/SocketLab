# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ChapterView.ui'
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
        self.horizontalLayout_4 = QHBoxLayout(Form)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
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

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.BookLabel = QLabel(Form)
        self.BookLabel.setObjectName(u"BookLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BookLabel.sizePolicy().hasHeightForWidth())
        self.BookLabel.setSizePolicy(sizePolicy)
        self.BookLabel.setFont(font)
        self.BookLabel.setTextFormat(Qt.MarkdownText)
        self.BookLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.BookLabel)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(Qt.MarkdownText)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(3)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setFont(font)
        self.label_3.setTextFormat(Qt.MarkdownText)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_3)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.ChapterListWidget = QListWidget(Form)
        self.ChapterListWidget.setObjectName(u"ChapterListWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.ChapterListWidget.sizePolicy().hasHeightForWidth())
        self.ChapterListWidget.setSizePolicy(sizePolicy2)
        self.ChapterListWidget.setFont(font)

        self.horizontalLayout_2.addWidget(self.ChapterListWidget)

        self.SynopsisTextEdit = QPlainTextEdit(Form)
        self.SynopsisTextEdit.setObjectName(u"SynopsisTextEdit")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(3)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.SynopsisTextEdit.sizePolicy().hasHeightForWidth())
        self.SynopsisTextEdit.setSizePolicy(sizePolicy3)
        self.SynopsisTextEdit.setFont(font)
        self.SynopsisTextEdit.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.SynopsisTextEdit)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"# Simple Reader -- Select Chapter", None))
        self.BookLabel.setText(QCoreApplication.translate("Form", u"## Book", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"## Chapters", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"## Synopsis", None))
        self.SynopsisTextEdit.setPlainText("")
    # retranslateUi
