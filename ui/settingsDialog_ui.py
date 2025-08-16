# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingsDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_settingsDialog(object):
    def setupUi(self, settingsDialog):
        if not settingsDialog.objectName():
            settingsDialog.setObjectName(u"settingsDialog")
        settingsDialog.resize(606, 284)
        settingsDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(settingsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.sheetSettingsHBoxLayout = QHBoxLayout()
        self.sheetSettingsHBoxLayout.setObjectName(u"sheetSettingsHBoxLayout")
        self.tourSheetSettings = QGroupBox(settingsDialog)
        self.tourSheetSettings.setObjectName(u"tourSheetSettings")
        self.formLayout = QFormLayout(self.tourSheetSettings)
        self.formLayout.setObjectName(u"formLayout")
        self.tourSheetNameLabel = QLabel(self.tourSheetSettings)
        self.tourSheetNameLabel.setObjectName(u"tourSheetNameLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.tourSheetNameLabel)

        self.tourSheetNameLineEdit = QLineEdit(self.tourSheetSettings)
        self.tourSheetNameLineEdit.setObjectName(u"tourSheetNameLineEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.tourSheetNameLineEdit)

        self.tourSheetStartRowLabel = QLabel(self.tourSheetSettings)
        self.tourSheetStartRowLabel.setObjectName(u"tourSheetStartRowLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.tourSheetStartRowLabel)

        self.tourSheetStartRowSpinBox = QSpinBox(self.tourSheetSettings)
        self.tourSheetStartRowSpinBox.setObjectName(u"tourSheetStartRowSpinBox")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.tourSheetStartRowSpinBox)

        self.tourSheetTourNameLabel = QLabel(self.tourSheetSettings)
        self.tourSheetTourNameLabel.setObjectName(u"tourSheetTourNameLabel")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.tourSheetTourNameLabel)

        self.tourSheetTourNameLineEdit = QLineEdit(self.tourSheetSettings)
        self.tourSheetTourNameLineEdit.setObjectName(u"tourSheetTourNameLineEdit")
        self.tourSheetTourNameLineEdit.setMaxLength(4)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.tourSheetTourNameLineEdit)

        self.tourSheetMapNameColumnLabel = QLabel(self.tourSheetSettings)
        self.tourSheetMapNameColumnLabel.setObjectName(u"tourSheetMapNameColumnLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.tourSheetMapNameColumnLabel)

        self.tourSheetMapNameColumnLineEdit = QLineEdit(self.tourSheetSettings)
        self.tourSheetMapNameColumnLineEdit.setObjectName(u"tourSheetMapNameColumnLineEdit")
        self.tourSheetMapNameColumnLineEdit.setMaxLength(4)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.tourSheetMapNameColumnLineEdit)


        self.sheetSettingsHBoxLayout.addWidget(self.tourSheetSettings)

        self.calcSheetSettings = QGroupBox(settingsDialog)
        self.calcSheetSettings.setObjectName(u"calcSheetSettings")
        self.formLayout_2 = QFormLayout(self.calcSheetSettings)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.calcSheetNameLabel = QLabel(self.calcSheetSettings)
        self.calcSheetNameLabel.setObjectName(u"calcSheetNameLabel")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.calcSheetNameLabel)

        self.calcSheetNameLineEdit = QLineEdit(self.calcSheetSettings)
        self.calcSheetNameLineEdit.setObjectName(u"calcSheetNameLineEdit")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.calcSheetNameLineEdit)

        self.calcSheetColumnLabel = QLabel(self.calcSheetSettings)
        self.calcSheetColumnLabel.setObjectName(u"calcSheetColumnLabel")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.calcSheetColumnLabel)

        self.calcSheetColumnLineEdit = QLineEdit(self.calcSheetSettings)
        self.calcSheetColumnLineEdit.setObjectName(u"calcSheetColumnLineEdit")
        self.calcSheetColumnLineEdit.setMaxLength(4)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.calcSheetColumnLineEdit)

        self.calcSheetRangeLabel = QLabel(self.calcSheetSettings)
        self.calcSheetRangeLabel.setObjectName(u"calcSheetRangeLabel")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.calcSheetRangeLabel)

        self.rangeSelectorLayout = QHBoxLayout()
        self.rangeSelectorLayout.setObjectName(u"rangeSelectorLayout")
        self.fromSpinbox = QSpinBox(self.calcSheetSettings)
        self.fromSpinbox.setObjectName(u"fromSpinbox")

        self.rangeSelectorLayout.addWidget(self.fromSpinbox)

        self.colonLabel = QLabel(self.calcSheetSettings)
        self.colonLabel.setObjectName(u"colonLabel")

        self.rangeSelectorLayout.addWidget(self.colonLabel)

        self.toSpinbox = QSpinBox(self.calcSheetSettings)
        self.toSpinbox.setObjectName(u"toSpinbox")

        self.rangeSelectorLayout.addWidget(self.toSpinbox)

        self.rangeSelectorLayout.setStretch(0, 1)
        self.rangeSelectorLayout.setStretch(2, 1)

        self.formLayout_2.setLayout(2, QFormLayout.ItemRole.FieldRole, self.rangeSelectorLayout)


        self.sheetSettingsHBoxLayout.addWidget(self.calcSheetSettings)


        self.verticalLayout.addLayout(self.sheetSettingsHBoxLayout)

        self.otherSettings = QGroupBox(settingsDialog)
        self.otherSettings.setObjectName(u"otherSettings")
        self.horizontalLayout_3 = QHBoxLayout(self.otherSettings)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.saveMapLocationLabel = QLabel(self.otherSettings)
        self.saveMapLocationLabel.setObjectName(u"saveMapLocationLabel")

        self.verticalLayout_2.addWidget(self.saveMapLocationLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.mapLocationLabel = QLabel(self.otherSettings)
        self.mapLocationLabel.setObjectName(u"mapLocationLabel")

        self.horizontalLayout_2.addWidget(self.mapLocationLabel)

        self.mapLocationButton = QPushButton(self.otherSettings)
        self.mapLocationButton.setObjectName(u"mapLocationButton")

        self.horizontalLayout_2.addWidget(self.mapLocationButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.saveMapLocationCheckBox = QCheckBox(self.otherSettings)
        self.saveMapLocationCheckBox.setObjectName(u"saveMapLocationCheckBox")
        self.saveMapLocationCheckBox.setChecked(True)

        self.verticalLayout_3.addWidget(self.saveMapLocationCheckBox)

        self.mapLocationLineEdit = QLineEdit(self.otherSettings)
        self.mapLocationLineEdit.setObjectName(u"mapLocationLineEdit")

        self.verticalLayout_3.addWidget(self.mapLocationLineEdit)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)


        self.verticalLayout.addWidget(self.otherSettings)

        self.buttonBox = QDialogButtonBox(settingsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)

        self.verticalLayout.setStretch(0, 1)
        QWidget.setTabOrder(self.tourSheetNameLineEdit, self.tourSheetStartRowSpinBox)
        QWidget.setTabOrder(self.tourSheetStartRowSpinBox, self.tourSheetTourNameLineEdit)
        QWidget.setTabOrder(self.tourSheetTourNameLineEdit, self.tourSheetMapNameColumnLineEdit)
        QWidget.setTabOrder(self.tourSheetMapNameColumnLineEdit, self.calcSheetNameLineEdit)
        QWidget.setTabOrder(self.calcSheetNameLineEdit, self.calcSheetColumnLineEdit)
        QWidget.setTabOrder(self.calcSheetColumnLineEdit, self.fromSpinbox)
        QWidget.setTabOrder(self.fromSpinbox, self.toSpinbox)

        self.retranslateUi(settingsDialog)

        QMetaObject.connectSlotsByName(settingsDialog)
    # setupUi

    def retranslateUi(self, settingsDialog):
        settingsDialog.setWindowTitle(QCoreApplication.translate("settingsDialog", u"Settings", None))
        self.tourSheetSettings.setTitle(QCoreApplication.translate("settingsDialog", u"Overview Sheet Settings", None))
        self.tourSheetNameLabel.setText(QCoreApplication.translate("settingsDialog", u"Overview Sheet Name", None))
        self.tourSheetNameLineEdit.setPlaceholderText(QCoreApplication.translate("settingsDialog", u"\u00dcbersicht", None))
        self.tourSheetStartRowLabel.setText(QCoreApplication.translate("settingsDialog", u"Overview Start Row", None))
        self.tourSheetTourNameLabel.setText(QCoreApplication.translate("settingsDialog", u"Tour Name Column", None))
        self.tourSheetTourNameLineEdit.setPlaceholderText(QCoreApplication.translate("settingsDialog", u"C", None))
        self.tourSheetMapNameColumnLabel.setText(QCoreApplication.translate("settingsDialog", u"Tour Map Name Column", None))
        self.tourSheetMapNameColumnLineEdit.setPlaceholderText(QCoreApplication.translate("settingsDialog", u"AP", None))
        self.calcSheetSettings.setTitle(QCoreApplication.translate("settingsDialog", u"Calculation Sheet Settings", None))
        self.calcSheetNameLabel.setText(QCoreApplication.translate("settingsDialog", u"Calculation Sheet Name", None))
        self.calcSheetNameLineEdit.setPlaceholderText(QCoreApplication.translate("settingsDialog", u"Berechnung", None))
        self.calcSheetColumnLabel.setText(QCoreApplication.translate("settingsDialog", u"Calculation Sheet Insertion Column", None))
        self.calcSheetColumnLineEdit.setPlaceholderText(QCoreApplication.translate("settingsDialog", u"B", None))
        self.calcSheetRangeLabel.setText(QCoreApplication.translate("settingsDialog", u"Calculation Row Range", None))
        self.colonLabel.setText(QCoreApplication.translate("settingsDialog", u":", None))
        self.otherSettings.setTitle(QCoreApplication.translate("settingsDialog", u"Map Settings", None))
        self.saveMapLocationLabel.setText(QCoreApplication.translate("settingsDialog", u"Save map location in Workbook", None))
        self.mapLocationLabel.setText(QCoreApplication.translate("settingsDialog", u"Map Location:", None))
        self.mapLocationButton.setText(QCoreApplication.translate("settingsDialog", u"Select File...", None))
        self.saveMapLocationCheckBox.setText("")
    # retranslateUi

