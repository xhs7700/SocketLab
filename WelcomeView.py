# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'WelcomeView.ui'
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
        self.horizontalLayout_3 = QHBoxLayout(Form)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.MarkdownText)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(Qt.MarkdownText)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(3)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy2)
        self.label_3.setFont(font)
        self.label_3.setTextFormat(Qt.MarkdownText)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_3)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.BookListWidget = QListWidget(Form)
        self.BookListWidget.setObjectName(u"BookListWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.BookListWidget.sizePolicy().hasHeightForWidth())
        self.BookListWidget.setSizePolicy(sizePolicy3)
        self.BookListWidget.setFont(font)

        self.horizontalLayout.addWidget(self.BookListWidget)

        self.SynopsisTextEdit = QPlainTextEdit(Form)
        self.SynopsisTextEdit.setObjectName(u"SynopsisTextEdit")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(3)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.SynopsisTextEdit.sizePolicy().hasHeightForWidth())
        self.SynopsisTextEdit.setSizePolicy(sizePolicy4)
        self.SynopsisTextEdit.setFont(font)
        self.SynopsisTextEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.SynopsisTextEdit)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"# Simple Reader -- Welcome", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"## Books", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"## Synopsis", None))
        self.SynopsisTextEdit.setPlainText(QCoreApplication.translate("Form",
                                                                      u"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus sed ex sed sapien efficitur pretium quis in sapien. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Pellentesque aliquet metus lacus. Nulla eu mauris rhoncus sapien laoreet iaculis. Aliquam iaculis facilisis justo tempor dapibus. Integer ultrices varius felis, a interdum neque viverra nec. Proin elementum quam sem. Integer ut luctus massa.\n"
                                                                      "\n"
                                                                      "Interdum et malesuada fames ac ante ipsum primis in faucibus. Maecenas eleifend ullamcorper orci, a feugiat massa vulputate fermentum. Morbi sollicitudin commodo lacus ut posuere. Sed sollicitudin posuere libero condimentum laoreet. Cras rutrum arcu diam, non pellentesque sapien eleifend sed. Interdum et malesuada fames ac ante ipsum primis in faucibus. Donec fringilla sem a nibh tincidunt maximus. Ut nisl justo, convallis sit amet ligula quis, vulputate rhoncus felis. Curabitur tincidunt, elit ac facilisis hendrerit, felis dui gravida sapien, suscipit semper l"
                                                                      "igula tortor at ante. Phasellus eleifend risus felis, et auctor ex vestibulum viverra.\n"
                                                                      "\n"
                                                                      "Praesent vel dapibus sem. Mauris non pulvinar lectus. Sed non dignissim purus. Morbi non nulla sem. Nulla dapibus, erat nec laoreet molestie, sapien ante rhoncus lorem, non auctor urna arcu at sapien. Pellentesque eget posuere ante, non bibendum lorem. Sed euismod non magna eu rutrum. Ut convallis quam arcu, in interdum massa egestas in. Cras sit amet erat velit. In feugiat felis vitae metus cursus, id porttitor odio pellentesque. Proin dictum metus eget tempor tempus. Sed et congue nunc, et tempus ligula. Cras sed ultrices ex. In quis odio nec erat volutpat consectetur. Proin sed lectus efficitur, cursus lectus rhoncus, commodo nunc.\n"
                                                                      "\n"
                                                                      "Donec molestie libero non sem condimentum, vel blandit ligula elementum. Donec at augue tristique, hendrerit enim vitae, placerat augue. Phasellus et efficitur nisl, non suscipit turpis. Integer vestibulum neque a sem efficitur mollis. Cras maximus nibh et urna pulvinar iaculi"
                                                                      "s. Nullam dapibus dui nec massa venenatis, sed volutpat tellus mollis. Proin interdum leo sit amet augue condimentum, non vestibulum metus accumsan.\n"
                                                                      "\n"
                                                                      "Curabitur et odio ligula. Aliquam pulvinar consequat venenatis. Duis nec posuere est. Pellentesque id lacinia lorem. In malesuada condimentum quam, eget viverra nulla finibus non. Nunc in vestibulum ligula. Aliquam in ex neque. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut nisl eros, pretium nec leo id, ultrices placerat dolor. Vestibulum porttitor, elit in interdum ultrices, metus sapien tempus justo, non sodales ligula mauris sed nibh. Donec rutrum imperdiet ex, eget egestas nunc maximus condimentum.\n"
                                                                      "\n"
                                                                      "", None))
    # retranslateUi
