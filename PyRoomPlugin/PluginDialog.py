#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PluginDialog.py
MIT License (c) Marie Faure <dev at faure dot systems>

Dialog to control PluginProps app running on Raspberry.
"""

import os, re

from PluginSettingsDialog import PluginSettingsDialog
from AppletDialog import AppletDialog
from LedWidget import LedWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QSize, QPoint, QSettings
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QFrame,
                             QPlainTextEdit, QPushButton, QSizePolicy, QComboBox, QLabel)


class PluginDialog(AppletDialog):
    aboutToClose = pyqtSignal()
    switchLed = pyqtSignal(str, str)

    # __________________________________________________________________
    def __init__(self, title, icon, logger):
        super().__init__(title, icon, logger)

        # always on top sometimes doesn't work
        self.setAttribute(Qt.WA_AlwaysStackOnTop)
        self.setWindowFlags(self.windowFlags()
                            & ~Qt.WindowContextHelpButtonHint | Qt.WindowStaysOnTopHint)

    # __________________________________________________________________
    def _buildUi(self):
        self._options = {}
        if os.path.isfile('definitions.ini'):
            definitions = QSettings('definitions.ini', QSettings.IniFormat)
            for group in definitions.childGroups():
                definitions.beginGroup(group)
                if group == "options":
                    for key in definitions.childKeys():
                        self._options[key] = definitions.value(key)
                definitions.endGroup()

        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)

        self._led = LedWidget(self.tr("Props name"), QSize(40, 20))
        self._led.setRedAsBold(True)
        self._led.setRedAsRed(True)
        self._led.switchOn('gray')

        settings_button = QPushButton()
        settings_button.setIcon(QIcon("./images/settings.svg"))
        settings_button.setFlat(True)
        settings_button.setToolTip(self.tr("Configuration"))
        settings_button.setIconSize(QSize(16, 16))
        settings_button.setFixedSize(QSize(24, 24))

        header_layout = QHBoxLayout()
        header_layout.addWidget(self._led)
        header_layout.addWidget(settings_button, Qt.AlignRight)
        main_layout.addLayout(header_layout)

        main_layout.addStretch(0)

        self.setLayout(main_layout)

        settings_button.pressed.connect(self.settings)
        self.switchLed.connect(self._led.switchOn)

    # __________________________________________________________________
    @pyqtSlot(str)
    def onPropsMessage(self, message):
        if message.startswith("DISCONNECTED"):
            self._led.switchOn('yellow')
        else:
            if self._led.color() != 'green':
                self._led.switchOn('green')

    # __________________________________________________________________
    def closeEvent(self, e):
        self.aboutToClose.emit()

    # __________________________________________________________________
    @pyqtSlot()
    def settings(self):
        dlg = PluginSettingsDialog(self._logger)
        dlg.setModal(True)
        dlg.move(self.pos() + QPoint(20, 20))
        dlg.exec()

