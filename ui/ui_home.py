# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'homeMkxhzF.ui'
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


class Ui_homeDialog(object):
    def setupUi(self, homeDialog):
        if homeDialog.objectName():
            homeDialog.setObjectName(u"homeDialog")
        homeDialog.resize(999, 588)
        homeDialog.setMinimumSize(QSize(143, 0))
        homeDialog.setMaximumSize(QSize(16677770, 16777215))
        homeDialog.setStyleSheet(u"")
        self.verticalLayoutWidget = QWidget(homeDialog)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(20, 20, 160, 531))
        self.sideMenuVL = QVBoxLayout(self.verticalLayoutWidget)
        self.sideMenuVL.setObjectName(u"sideMenuVL")
        self.sideMenuVL.setContentsMargins(0, 0, 0, 0)
        self.sidebarBackgroud = QWidget(self.verticalLayoutWidget)
        self.sidebarBackgroud.setObjectName(u"sidebarBackgroud")
        self.sidebarBackgroud.setStyleSheet(u"background-color: rgb(38, 38, 38);border-radius: 15px;")
        self.sidebarHome = QLabel(self.sidebarBackgroud)
        self.sidebarHome.setObjectName(u"sidebarHome")
        self.sidebarHome.setGeometry(QRect(0, 20, 158, 41))
        self.sidebarHome.setStyleSheet(u"background-color: rgb(70, 70, 70);border-radius: 15px;font:15pt;\n"
"color: rgb(255, 255, 255);")
        self.sidebarHome.setAlignment(Qt.AlignCenter)
        self.sidebarTransactions = QLabel(self.sidebarBackgroud)
        self.sidebarTransactions.setObjectName(u"sidebarTransactions")
        self.sidebarTransactions.setGeometry(QRect(0, 80, 158, 41))
        self.sidebarTransactions.setStyleSheet(u"background-color: rgb(70, 70, 70);border-radius: 15px;font:15pt;color:white;")
        self.sidebarTransactions.setAlignment(Qt.AlignCenter)
        self.sidebarCalendar = QLabel(self.sidebarBackgroud)
        self.sidebarCalendar.setObjectName(u"sidebarCalendar")
        self.sidebarCalendar.setGeometry(QRect(0, 140, 158, 41))
        self.sidebarCalendar.setStyleSheet(u"background-color: rgb(70, 70, 70);border-radius: 15px;font:15pt;color:white;")
        self.sidebarCalendar.setAlignment(Qt.AlignCenter)

        self.sideMenuVL.addWidget(self.sidebarBackgroud)

        self.homeTiltle = QLabel(homeDialog)
        self.homeTiltle.setObjectName(u"homeTiltle")
        self.homeTiltle.setGeometry(QRect(200, 20, 158, 41))
        self.homeTiltle.setStyleSheet(u"background-color: rgb(70, 70, 70);border-radius: 15px;font:15pt;color:white;")
        self.homeTiltle.setAlignment(Qt.AlignCenter)
        self.addAccBtn = QPushButton(homeDialog)
        self.addAccBtn.setObjectName(u"addAccBtn")
        self.addAccBtn.setGeometry(QRect(800, 480, 71, 61))
        self.addAccBtn.setStyleSheet(u"background-color: rgb(170, 0, 0);border-radius: 15px;font-size:30px;")
        self.addAccBtn.setAutoDefault(False)
        self.accScrollArea = QScrollArea(homeDialog)
        self.accScrollArea.setObjectName(u"accScrollArea")
        self.accScrollArea.setGeometry(QRect(190, 70, 701, 171))
        self.accScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 699, 169))
        self.layoutWidget = QWidget(self.scrollAreaWidgetContents)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 701, 171))
        self.accHL = QHBoxLayout(self.layoutWidget)
        self.accHL.setObjectName(u"accHL")
        self.accHL.setContentsMargins(0, 0, 0, 0)
        self.accScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.testPushButton = QPushButton(homeDialog)
        self.testPushButton.setObjectName(u"testPushButton")
        self.testPushButton.setGeometry(QRect(310, 480, 111, 51))

        self.retranslateUi(homeDialog)

        self.addAccBtn.setDefault(False)


        QMetaObject.connectSlotsByName(homeDialog)
    # setupUi

    def retranslateUi(self, homeDialog):
        homeDialog.setWindowTitle(QCoreApplication.translate("homeDialog", u"Dialog", None))
#if QT_CONFIG(tooltip)
        homeDialog.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.sidebarHome.setText(QCoreApplication.translate("homeDialog", u"Home", None))
        self.sidebarTransactions.setText(QCoreApplication.translate("homeDialog", u"Transactions", None))
        self.sidebarCalendar.setText(QCoreApplication.translate("homeDialog", u"Calendar", None))
        self.homeTiltle.setText(QCoreApplication.translate("homeDialog", u"Home", None))
#if QT_CONFIG(tooltip)
        self.addAccBtn.setToolTip(QCoreApplication.translate("homeDialog", u"Add Account", None))
#endif // QT_CONFIG(tooltip)
        self.addAccBtn.setText(QCoreApplication.translate("homeDialog", u"+", None))
        self.testPushButton.setText(QCoreApplication.translate("homeDialog", u"test", None))
    # retranslateUi

