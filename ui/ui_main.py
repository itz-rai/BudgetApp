# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainJHFlBC.ui'
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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 600)
        MainWindow.setStyleSheet(u"background-color: rgb(61, 61, 61);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.login = QLabel(self.centralwidget)
        self.login.setObjectName(u"login")
        self.login.setGeometry(QRect(270, 60, 191, 51))
        self.login.setStyleSheet(u"color: rgb(255, 255, 255);font-size:24pt;")
        self.login.setAlignment(Qt.AlignCenter)
        self.username = QLabel(self.centralwidget)
        self.username.setObjectName(u"username")
        self.username.setGeometry(QRect(50, 170, 161, 31))
        self.username.setStyleSheet(u"color: rgb(255, 255, 255);font-size:20pt;")
        self.password = QLabel(self.centralwidget)
        self.password.setObjectName(u"password")
        self.password.setGeometry(QRect(50, 230, 161, 31))
        self.password.setStyleSheet(u"color: rgb(255, 255, 255);font-size:20pt;")
        self.userNameInput = QLineEdit(self.centralwidget)
        self.userNameInput.setObjectName(u"userNameInput")
        self.userNameInput.setGeometry(QRect(220, 170, 371, 41))
        self.passwordInput = QLineEdit(self.centralwidget)
        self.passwordInput.setObjectName(u"passwordInput")
        self.passwordInput.setGeometry(QRect(220, 230, 371, 41))
        self.loginbutton = QPushButton(self.centralwidget)
        self.loginbutton.setObjectName(u"loginbutton")
        self.loginbutton.setGeometry(QRect(480, 360, 171, 61))
        self.loginbutton.setStyleSheet(u"background-color: rgb(0, 95, 95);")
        self.guest = QPushButton(self.centralwidget)
        self.guest.setObjectName(u"guest")
        self.guest.setGeometry(QRect(40, 360, 171, 61))
        self.guest.setStyleSheet(u"background-color: rgb(0, 95, 95);")
        self.create = QPushButton(self.centralwidget)
        self.create.setObjectName(u"create")
        self.create.setGeometry(QRect(260, 360, 171, 61))
        self.create.setStyleSheet(u"background-color: rgb(0, 95, 95);")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.login.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.username.setText(QCoreApplication.translate("MainWindow", u"User Name:", None))
        self.password.setText(QCoreApplication.translate("MainWindow", u"Password:", None))
        self.loginbutton.setText(QCoreApplication.translate("MainWindow", u"Log In", None))
        self.guest.setText(QCoreApplication.translate("MainWindow", u"Guest Account", None))
        self.create.setText(QCoreApplication.translate("MainWindow", u"Create Account", None))
    # retranslateUi

