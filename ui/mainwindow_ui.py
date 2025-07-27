# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 601)
        self.actionLoad_KML = QAction(MainWindow)
        self.actionLoad_KML.setObjectName(u"actionLoad_KML")
        self.actionReload = QAction(MainWindow)
        self.actionReload.setObjectName(u"actionReload")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionExit.setMenuRole(QAction.MenuRole.QuitRole)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionAbout.setMenuRole(QAction.MenuRole.AboutRole)
        self.actionAbout_Qt = QAction(MainWindow)
        self.actionAbout_Qt.setObjectName(u"actionAbout_Qt")
        self.actionAbout_Qt.setMenuRole(QAction.MenuRole.AboutQtRole)
        self.actionOpen_Excel = QAction(MainWindow)
        self.actionOpen_Excel.setObjectName(u"actionOpen_Excel")
        self.actionReset_Highlight = QAction(MainWindow)
        self.actionReset_Highlight.setObjectName(u"actionReset_Highlight")
        self.actionReset_Highlight.setCheckable(False)
        self.actionHighlighting_Test = QAction(MainWindow)
        self.actionHighlighting_Test.setObjectName(u"actionHighlighting_Test")
        self.actionHighlighting_Test.setCheckable(True)
        self.actionShow_Statusbar = QAction(MainWindow)
        self.actionShow_Statusbar.setObjectName(u"actionShow_Statusbar")
        self.actionShow_Statusbar.setCheckable(True)
        self.actionShow_Statusbar.setChecked(True)
        self.actionWorkbook_Settings = QAction(MainWindow)
        self.actionWorkbook_Settings.setObjectName(u"actionWorkbook_Settings")
        self.actionWorkbook_Settings.setEnabled(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.webEngineView = QWebEngineView(self.centralwidget)
        self.webEngineView.setObjectName(u"webEngineView")
        self.webEngineView.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.webEngineView.setUrl(QUrl(u"about:blank"))

        self.gridLayout.addWidget(self.webEngineView, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuDebug = QMenu(self.menubar)
        self.menuDebug.setObjectName(u"menuDebug")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setEnabled(True)
        self.statusbar.setSizeGripEnabled(True)
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuDebug.menuAction())
        self.menuFile.addAction(self.actionOpen_Excel)
        self.menuFile.addAction(self.actionWorkbook_Settings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionAbout_Qt)
        self.menuDebug.addAction(self.actionLoad_KML)
        self.menuDebug.addAction(self.actionReload)
        self.menuDebug.addSeparator()
        self.menuDebug.addAction(self.actionHighlighting_Test)
        self.menuDebug.addAction(self.actionReset_Highlight)
        self.menuDebug.addSeparator()
        self.menuDebug.addAction(self.actionShow_Statusbar)

        self.retranslateUi(MainWindow)
        self.actionShow_Statusbar.toggled.connect(self.statusbar.setVisible)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionLoad_KML.setText(QCoreApplication.translate("MainWindow", u"Load KML...", None))
        self.actionReload.setText(QCoreApplication.translate("MainWindow", u"Reload", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About...", None))
        self.actionAbout_Qt.setText(QCoreApplication.translate("MainWindow", u"About Qt...", None))
        self.actionOpen_Excel.setText(QCoreApplication.translate("MainWindow", u"Open Excel...", None))
        self.actionReset_Highlight.setText(QCoreApplication.translate("MainWindow", u"Reset Highlight", None))
        self.actionHighlighting_Test.setText(QCoreApplication.translate("MainWindow", u"Highlighting Test", None))
        self.actionShow_Statusbar.setText(QCoreApplication.translate("MainWindow", u"Show Statusbar", None))
        self.actionWorkbook_Settings.setText(QCoreApplication.translate("MainWindow", u"Workbook Settings...", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuDebug.setTitle(QCoreApplication.translate("MainWindow", u"Debug", None))
    # retranslateUi

