# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'addAccountDialogqYYmoa.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_createAccountDialog(object):
    def setupUi(self, createAccountDialog):
        if createAccountDialog.objectName():
            createAccountDialog.setObjectName(u"createAccountDialog")
        createAccountDialog.resize(468, 409)
        createAccountDialog.setStyleSheet(u"\n"
"QDialog {\n"
"    background-color: rgb(98, 98, 98);\n"
"}\n"
"\n"
"QLineEdit {\n"
"    border: 1px solid black;\n"
"    border-radius: 10px;\n"
"    height: 35px;\n"
"}\n"
"")
        self.line = QFrame(createAccountDialog)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(-10, 50, 511, 16))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.addNewAccount = QLabel(createAccountDialog)
        self.addNewAccount.setObjectName(u"addNewAccount")
        self.addNewAccount.setGeometry(QRect(110, 10, 251, 41))
        font = QFont()
        font.setFamily(u"Leelawadee UI")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.addNewAccount.setFont(font)
        self.addNewAccBtn = QPushButton(createAccountDialog)
        self.addNewAccBtn.setObjectName(u"addNewAccBtn")
        self.addNewAccBtn.setGeometry(QRect(40, 270, 101, 31))
        self.closeAddAccountDialogBtn = QPushButton(createAccountDialog)
        self.closeAddAccountDialogBtn.setObjectName(u"closeAddAccountDialogBtn")
        self.closeAddAccountDialogBtn.setGeometry(QRect(340, 270, 101, 31))
        self.layoutWidget = QWidget(createAccountDialog)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(30, 90, 411, 144))
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.accNameLbl = QLabel(self.layoutWidget)
        self.accNameLbl.setObjectName(u"accNameLbl")
        font1 = QFont()
        font1.setPointSize(16)
        self.accNameLbl.setFont(font1)

        self.verticalLayout.addWidget(self.accNameLbl)

        self.accNameLe = QLineEdit(self.layoutWidget)
        self.accNameLe.setObjectName(u"accNameLe")
        self.accNameLe.setMinimumSize(QSize(0, 35))
        self.accNameLe.setMaximumSize(QSize(16777215, 35))
        self.accNameLe.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.accNameLe)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.accBalanceLbl = QLabel(self.layoutWidget)
        self.accBalanceLbl.setObjectName(u"accBalanceLbl")
        self.accBalanceLbl.setFont(font1)

        self.verticalLayout_2.addWidget(self.accBalanceLbl)

        self.accBalanceLe = QLineEdit(self.layoutWidget)
        self.accBalanceLe.setObjectName(u"accBalanceLe")
        self.accBalanceLe.setMinimumSize(QSize(0, 35))
        self.accBalanceLe.setMaximumSize(QSize(16777215, 35))
        self.accBalanceLe.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.accBalanceLe)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.retranslateUi(createAccountDialog)

        QMetaObject.connectSlotsByName(createAccountDialog)
    # setupUi

    def retranslateUi(self, createAccountDialog):
        createAccountDialog.setWindowTitle(QCoreApplication.translate("createAccountDialog", u"Dialog", None))
        self.addNewAccount.setText(QCoreApplication.translate("createAccountDialog", u"Add New Account", None))
        self.addNewAccBtn.setText(QCoreApplication.translate("createAccountDialog", u"Add new Account", None))
        self.closeAddAccountDialogBtn.setText(QCoreApplication.translate("createAccountDialog", u"Cancel", None))
        self.accNameLbl.setText(QCoreApplication.translate("createAccountDialog", u"Name of Account:", None))
        self.accNameLe.setText("")
        self.accBalanceLbl.setText(QCoreApplication.translate("createAccountDialog", u"Balance on Account:", None))
        self.accBalanceLe.setText("")
    # retranslateUi

