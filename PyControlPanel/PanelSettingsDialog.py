#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PanelSettingsDialog.py
MIT License (c) Marie Faure <dev at faure dot systems>

Dialog to configure panel parameters.
"""

import os
import codecs
import configparser

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtWidgets import QDialog, QRadioButton, QPushButton, QGroupBox
from PyQt5.QtGui import QIcon


class PanelSettingsDialog(QDialog):

    # __________________________________________________________________
    def __init__(self, settings, logger):

        super(PanelSettingsDialog, self).__init__()

        self._logger = logger
        self._settings = settings

        self.setAttribute(Qt.WA_AlwaysStackOnTop)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle(self.tr("Settings"))
        self.setWindowIcon(QIcon('./images/settings.svg'))
        self.buildUi()

    # __________________________________________________________________
    def buildUi(self):

        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)

        param_box = QGroupBox(self.tr("Configuration"))
        param_box_layout = QVBoxLayout(param_box)
        main_layout.addWidget(param_box)

        param1_button = QRadioButton(self.tr("Parameter 1"))
        param2_button = QRadioButton(self.tr("Parameter 2"))
        param_box_layout.addWidget(param1_button)
        param_box_layout.addWidget(param2_button)

        if 'param' in self._settings['parameters']:
            param = self._settings['parameters']['param']
        else:
            param = "1"

        if param == "2":
            param2_button.setChecked(True)
        else:
            param1_button.setChecked(True)

        close_button = QPushButton(self.tr("Close"))
        close_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        param1_button.pressed.connect(self.setParameters1)
        param2_button.pressed.connect(self.setParameters2)
        close_button.pressed.connect(self.accept)

    # __________________________________________________________________
    @pyqtSlot()
    def setParameters1(self):

        self._logger.info(self.tr("Settings : set 'param' parameters"))
        self._settings['parameters']['param'] = "1"

    # __________________________________________________________________
    @pyqtSlot()
    def setParameters2(self):

        self._logger.info(self.tr("Settings : set 'param' parameters"))
        self._settings['parameters']['param'] = "2"
