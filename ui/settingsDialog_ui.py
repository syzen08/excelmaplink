# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settingsDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

class Ui_settingsDialog(object):
    def setupUi(self, settingsDialog):
        if not settingsDialog.objectName():
            settingsDialog.setObjectName(u"settingsDialog")
        settingsDialog.resize(600, 256)
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

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.tourSheetNameLabel)

        self.tourSheetNameLineEdit = QLineEdit(self.tourSheetSettings)
        self.tourSheetNameLineEdit.setObjectName(u"tourSheetNameLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.tourSheetNameLineEdit)

        self.tourSheetMapNameColumnLineEdit = QLineEdit(self.tourSheetSettings)
        self.tourSheetMapNameColumnLineEdit.setObjectName(u"tourSheetMapNameColumnLineEdit")
        self.tourSheetMapNameColumnLineEdit.setMaxLength(4)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.tourSheetMapNameColumnLineEdit)

        self.tourSheetStartRowLabel = QLabel(self.tourSheetSettings)
        self.tourSheetStartRowLabel.setObjectName(u"tourSheetStartRowLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.tourSheetStartRowLabel)

        self.tourSheetMapNameColumnLabel = QLabel(self.tourSheetSettings)
        self.tourSheetMapNameColumnLabel.setObjectName(u"tourSheetMapNameColumnLabel")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.tourSheetMapNameColumnLabel)

        self.tourSheetStartRowSpinBox = QSpinBox(self.tourSheetSettings)
        self.tourSheetStartRowSpinBox.setObjectName(u"tourSheetStartRowSpinBox")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.tourSheetStartRowSpinBox)

        self.tourSheetTourNameLabel = QLabel(self.tourSheetSettings)
        self.tourSheetTourNameLabel.setObjectName(u"tourSheetTourNameLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.tourSheetTourNameLabel)

        self.tourSheetTourNameLineEdit = QLineEdit(self.tourSheetSettings)
        self.tourSheetTourNameLineEdit.setObjectName(u"tourSheetTourNameLineEdit")
        self.tourSheetTourNameLineEdit.setMaxLength(4)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.tourSheetTourNameLineEdit)


        self.sheetSettingsHBoxLayout.addWidget(self.tourSheetSettings)

        self.calcSheetSettings = QGroupBox(settingsDialog)
        self.calcSheetSettings.setObjectName(u"calcSheetSettings")
        self.formLayout_2 = QFormLayout(self.calcSheetSettings)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.calcSheetNameLabel = QLabel(self.calcSheetSettings)
        self.calcSheetNameLabel.setObjectName(u"calcSheetNameLabel")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.calcSheetNameLabel)

        self.calcSheetNameLineEdit = QLineEdit(self.calcSheetSettings)
        self.calcSheetNameLineEdit.setObjectName(u"calcSheetNameLineEdit")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.calcSheetNameLineEdit)

        self.calcSheetColumnLabel = QLabel(self.calcSheetSettings)
        self.calcSheetColumnLabel.setObjectName(u"calcSheetColumnLabel")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.calcSheetColumnLabel)

        self.calcSheetColumnLineEdit = QLineEdit(self.calcSheetSettings)
        self.calcSheetColumnLineEdit.setObjectName(u"calcSheetColumnLineEdit")
        self.calcSheetColumnLineEdit.setMaxLength(4)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.calcSheetColumnLineEdit)

        self.calcSheetRangeLabel = QLabel(self.calcSheetSettings)
        self.calcSheetRangeLabel.setObjectName(u"calcSheetRangeLabel")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.calcSheetRangeLabel)

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

        self.formLayout_2.setLayout(2, QFormLayout.FieldRole, self.rangeSelectorLayout)


        self.sheetSettingsHBoxLayout.addWidget(self.calcSheetSettings)


        self.verticalLayout.addLayout(self.sheetSettingsHBoxLayout)

        self.otherSettings = QGroupBox(settingsDialog)
        self.otherSettings.setObjectName(u"otherSettings")
        self.gridLayout = QGridLayout(self.otherSettings)
        self.gridLayout.setObjectName(u"gridLayout")
        self.saveMapLocationCheckBox = QCheckBox(self.otherSettings)
        self.saveMapLocationCheckBox.setObjectName(u"saveMapLocationCheckBox")

        self.gridLayout.addWidget(self.saveMapLocationCheckBox, 0, 1, 1, 1)

        self.saveMapLocationLabel = QLabel(self.otherSettings)
        self.saveMapLocationLabel.setObjectName(u"saveMapLocationLabel")

        self.gridLayout.addWidget(self.saveMapLocationLabel, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 2, 1, 1)


        self.verticalLayout.addWidget(self.otherSettings)

        self.buttonBox = QDialogButtonBox(settingsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)

        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(settingsDialog)

        QMetaObject.connectSlotsByName(settingsDialog)
    # setupUi

    def retranslateUi(self, settingsDialog):
        settingsDialog.setWindowTitle(QCoreApplication.translate("settingsDialog", u"Settings", None))
        self.tourSheetSettings.setTitle(QCoreApplication.translate("settingsDialog", u"Overview Sheet Settings", None))
        self.tourSheetNameLabel.setText(QCoreApplication.translate("settingsDialog", u"Overview Sheet Name", None))
        self.tourSheetNameLineEdit.setPlaceholderText(QCoreApplication.translate("settingsDialog", u"\u00dcbersicht", None))
        self.tourSheetMapNameColumnLineEdit.setPlaceholderText(QCoreApplication.translate("settingsDialog", u"AP", None))
        self.tourSheetStartRowLabel.setText(QCoreApplication.translate("settingsDialog", u"Overview Start Row", None))
        self.tourSheetMapNameColumnLabel.setText(QCoreApplication.translate("settingsDialog", u"Tour Map Name Column", None))
        self.tourSheetTourNameLabel.setText(QCoreApplication.translate("settingsDialog", u"Tour Name Column", None))
        self.tourSheetTourNameLineEdit.setInputMask("")
        self.tourSheetTourNameLineEdit.setPlaceholderText(QCoreApplication.translate("settingsDialog", u"C", None))
        self.calcSheetSettings.setTitle(QCoreApplication.translate("settingsDialog", u"Calculation Sheet Settings", None))
        self.calcSheetNameLabel.setText(QCoreApplication.translate("settingsDialog", u"Calculation Sheet Name", None))
        self.calcSheetNameLineEdit.setPlaceholderText(QCoreApplication.translate("settingsDialog", u"Berechnung", None))
        self.calcSheetColumnLabel.setText(QCoreApplication.translate("settingsDialog", u"Calculation Sheet Insertion Column", None))
        self.calcSheetColumnLineEdit.setPlaceholderText(QCoreApplication.translate("settingsDialog", u"B", None))
        self.calcSheetRangeLabel.setText(QCoreApplication.translate("settingsDialog", u"Calculation Row Range", None))
        self.colonLabel.setText(QCoreApplication.translate("settingsDialog", u":", None))
        self.otherSettings.setTitle(QCoreApplication.translate("settingsDialog", u"Other Settings", None))
        self.saveMapLocationCheckBox.setText("")
        self.saveMapLocationLabel.setText(QCoreApplication.translate("settingsDialog", u"Save map location in Workbook", None))
    # retranslateUi

