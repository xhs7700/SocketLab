# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RegisterView.ui'
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
        self.gridLayout.setContentsMargins(150, 150, 150, 150)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.MarkdownText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)

        self.RegSubmitBtn = QPushButton(Form)
        self.RegSubmitBtn.setObjectName(u"RegSubmitBtn")
        self.RegSubmitBtn.setEnabled(False)
        self.RegSubmitBtn.setFont(font)

        self.gridLayout.addWidget(self.RegSubmitBtn, 6, 2, 1, 1)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.EmailInput = QLineEdit(Form)
        self.EmailInput.setObjectName(u"EmailInput")
        self.EmailInput.setFont(font)
        self.EmailInput.setEchoMode(QLineEdit.Normal)

        self.gridLayout.addWidget(self.EmailInput, 2, 1, 1, 2)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.UidInput = QLineEdit(Form)
        self.UidInput.setObjectName(u"UidInput")
        self.UidInput.setFont(font)

        self.gridLayout.addWidget(self.UidInput, 1, 1, 1, 2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 6, 1, 1, 1)

        self.RepPswInput = QLineEdit(Form)
        self.RepPswInput.setObjectName(u"RepPswInput")
        self.RepPswInput.setFont(font)
        self.RepPswInput.setEchoMode(QLineEdit.Password)

        self.gridLayout.addWidget(self.RepPswInput, 4, 1, 1, 1)

        self.PswInput = QLineEdit(Form)
        self.PswInput.setObjectName(u"PswInput")
        self.PswInput.setFont(font)
        self.PswInput.setEchoMode(QLineEdit.Password)

        self.gridLayout.addWidget(self.PswInput, 3, 1, 1, 1)

        self.RepPswChecker = QCheckBox(Form)
        self.RepPswChecker.setObjectName(u"RepPswChecker")
        self.RepPswChecker.setEnabled(False)
        self.RepPswChecker.setFont(font)

        self.gridLayout.addWidget(self.RepPswChecker, 3, 2, 2, 1)

        self.horizontalLayout.addLayout(self.gridLayout)

        QWidget.setTabOrder(self.UidInput, self.EmailInput)
        QWidget.setTabOrder(self.EmailInput, self.PswInput)
        QWidget.setTabOrder(self.PswInput, self.RepPswInput)
        QWidget.setTabOrder(self.RepPswInput, self.RegSubmitBtn)
        QWidget.setTabOrder(self.RegSubmitBtn, self.RepPswChecker)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"# Simple Reader -- Register", None))
        self.RegSubmitBtn.setText(QCoreApplication.translate("Form", u"Submit", None))
        # if QT_CONFIG(shortcut)
        self.RegSubmitBtn.setShortcut(QCoreApplication.translate("Form", u"Return", None))
        # endif // QT_CONFIG(shortcut)
        self.label_4.setText(QCoreApplication.translate("Form", u"Repeat Password", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"User ID", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Password", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Email", None))
        self.RepPswChecker.setText(QCoreApplication.translate("Form", u"Two Input Match", None))
    # retranslateUi
