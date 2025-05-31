# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'progressDialogMUcQBg.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QProgressBar,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_progressDialog(object):
    def setupUi(self, progressDialog):
        if not progressDialog.objectName():
            progressDialog.setObjectName(u"progressDialog")
        progressDialog.resize(420, 64)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(progressDialog.sizePolicy().hasHeightForWidth())
        progressDialog.setSizePolicy(sizePolicy)
        progressDialog.setMinimumSize(QSize(420, 64))
        progressDialog.setMaximumSize(QSize(420, 64))
        progressDialog.setBaseSize(QSize(420, 64))
        progressDialog.setCursor(QCursor(Qt.CursorShape.WaitCursor))
        progressDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(progressDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.message = QLabel(progressDialog)
        self.message.setObjectName(u"message")
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.message)

        self.progressBar = QProgressBar(progressDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(False)

        self.verticalLayout.addWidget(self.progressBar)


        self.retranslateUi(progressDialog)

        QMetaObject.connectSlotsByName(progressDialog)
    # setupUi

    def retranslateUi(self, progressDialog):
        progressDialog.setWindowTitle(QCoreApplication.translate("progressDialog", u"Dialog", None))
        self.message.setText(QCoreApplication.translate("progressDialog", u"TextLabel", None))
    # retranslateUi

