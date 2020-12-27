# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LoginView.ui'
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
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(200, 150, 200, 150)
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.UidInput = QLineEdit(Form)
        self.UidInput.setObjectName(u"UidInput")
        self.UidInput.setFont(font)

        self.gridLayout.addWidget(self.UidInput, 1, 1, 1, 1)

        self.PswInput = QLineEdit(Form)
        self.PswInput.setObjectName(u"PswInput")
        self.PswInput.setFont(font)
        self.PswInput.setEchoMode(QLineEdit.Password)

        self.gridLayout.addWidget(self.PswInput, 2, 1, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.RegBtn = QPushButton(Form)
        self.RegBtn.setObjectName(u"RegBtn")
        self.RegBtn.setFont(font)

        self.gridLayout.addWidget(self.RegBtn, 3, 0, 1, 1)

        self.LoginBtn = QPushButton(Form)
        self.LoginBtn.setObjectName(u"LoginBtn")
        self.LoginBtn.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LoginBtn.sizePolicy().hasHeightForWidth())
        self.LoginBtn.setSizePolicy(sizePolicy)
        self.LoginBtn.setFont(font)

        self.gridLayout.addWidget(self.LoginBtn, 3, 1, 1, 1)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setFont(font)
        self.label_3.setTextFormat(Qt.MarkdownText)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 2)

        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Password", None))
        self.label.setText(QCoreApplication.translate("Form", u"User ID", None))
        self.RegBtn.setText(QCoreApplication.translate("Form", u"&Register", None))
        # if QT_CONFIG(shortcut)
        self.RegBtn.setShortcut(QCoreApplication.translate("Form", u"Alt+R", None))
        # endif // QT_CONFIG(shortcut)
        self.LoginBtn.setText(QCoreApplication.translate("Form", u"Login", None))
        # if QT_CONFIG(shortcut)
        self.LoginBtn.setShortcut(QCoreApplication.translate("Form", u"Return", None))
        # endif // QT_CONFIG(shortcut)
        self.label_3.setText(QCoreApplication.translate("Form", u"# Simple Reader -- Login", None))
    # retranslateUi
