# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'aboutDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_aboutDialog(object):
    def setupUi(self, aboutDialog):
        if not aboutDialog.objectName():
            aboutDialog.setObjectName(u"aboutDialog")
        aboutDialog.resize(651, 254)
        self.gridLayout = QGridLayout(aboutDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.copyrightLabel = QLabel(aboutDialog)
        self.copyrightLabel.setObjectName(u"copyrightLabel")

        self.gridLayout.addWidget(self.copyrightLabel, 5, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 307, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 5, 0, 1, 1)

        self.iconLabel = QLabel(aboutDialog)
        self.iconLabel.setObjectName(u"iconLabel")
        self.iconLabel.setMaximumSize(QSize(192, 192))
        self.iconLabel.setPixmap(QPixmap(u":/icons/icon.png"))
        self.iconLabel.setScaledContents(True)

        self.gridLayout.addWidget(self.iconLabel, 4, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.titleLabel = QLabel(aboutDialog)
        self.titleLabel.setObjectName(u"titleLabel")

        self.verticalLayout.addWidget(self.titleLabel)

        self.versionLabel = QLabel(aboutDialog)
        self.versionLabel.setObjectName(u"versionLabel")
        self.versionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.versionLabel)

        self.commitLabel = QLabel(aboutDialog)
        self.commitLabel.setObjectName(u"commitLabel")
        self.commitLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.commitLabel)

        self.label = QLabel(aboutDialog)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setOpenExternalLinks(True)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.verticalLayout.addWidget(self.label)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.gridLayout.addLayout(self.verticalLayout, 4, 2, 1, 1)


        self.retranslateUi(aboutDialog)

        QMetaObject.connectSlotsByName(aboutDialog)
    # setupUi

    def retranslateUi(self, aboutDialog):
        aboutDialog.setWindowTitle(QCoreApplication.translate("aboutDialog", u"About", None))
        self.copyrightLabel.setText(QCoreApplication.translate("aboutDialog", u"\u00a9 2025 David Barthel", None))
        self.iconLabel.setText("")
        self.titleLabel.setText(QCoreApplication.translate("aboutDialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:700;\">excelmaplink</span></p></body></html>", None))
        self.versionLabel.setText(QCoreApplication.translate("aboutDialog", u"Version: dev", None))
        self.commitLabel.setText(QCoreApplication.translate("aboutDialog", u"Commit: dev", None))
        self.label.setText(QCoreApplication.translate("aboutDialog", u"<html><head/><body><p><a href=\"https://github.com/syzen08/excelmaplink\"><span style=\" text-decoration: underline; color:#0e6dc6;\">Website</span></a></p></body></html>", None))
    # retranslateUi

