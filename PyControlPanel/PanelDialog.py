#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PanelDialog.py
MIT License (c) Marie Faure <dev at faure dot systems>

Dialog to control PanelProps app running on Raspberry.
"""

import os
import codecs
import configparser
import re

from constants import *
from PanelSettingsDialog import PanelSettingsDialog
from AppletDialog import AppletDialog
from DataWidget import DataWidget
from LedWidget import LedWidget

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QSize, QPoint
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QGroupBox


class PanelDialog(AppletDialog):
    aboutToClose = pyqtSignal()
    propDataReveived = pyqtSignal(dict)
    publishMessage = pyqtSignal(str, str)
    switchLed = pyqtSignal(str, str)

    # __________________________________________________________________
    def __init__(self, title, icon, prop_outbox, logger):

        super().__init__(title, icon, logger)

        self._propOutbox = prop_outbox
        self._reDataSplitValues = re.compile(r'[^\s]+\s*=')
        self._reDataVariables = re.compile(r'([^\s]+)\s*=')

        # always on top sometimes doesn't work
        self.setAttribute(Qt.WA_AlwaysStackOnTop)
        self.setWindowFlags(self.windowFlags()
                            & ~Qt.WindowContextHelpButtonHint | Qt.WindowStaysOnTopHint)

    # __________________________________________________________________
    def _buildUi(self):

        self._settings = configparser.ConfigParser()
        ini = 'settings.ini'
        if os.path.isfile(ini):
            self._settings.read_file(codecs.open(ini, 'r', 'utf8'))

        if 'parameters' not in self._settings.sections():
            self._settings.add_section('parameters')

        if 'param' not in self._settings['parameters']:
            self._settings['parameters']['param'] = "1"  # default, values must be string

        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)

        self._led = LedWidget(PROP_NAME, QSize(40, 20))
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

        box = QGroupBox(self.tr(""))
        box_layout = QVBoxLayout(box)
        box_layout.setSpacing(12)
        main_layout.addWidget(box)

        dataLed_options = {}
        dataLed_options['image_on'] = DATALED_IMAGE_ON
        dataLed_options['image_off'] = DATALED_IMAGE_OFF

        self._dataLed = DataWidget(self.tr("Led"), 'led', options=dataLed_options, label_width=LABELS_WIDTH)
        box_layout.addWidget(self._dataLed)

        main_layout.addStretch(0)

        self.setLayout(main_layout)

        settings_button.pressed.connect(self.onSettingsButton)
        self.switchLed.connect(self._led.switchOn)

        self.propDataReveived.connect(self._dataLed.onDataReceived)

    # __________________________________________________________________
    def _parsePropData(self, message):

        variables = {}
        data = message[5:]
        vars = re.split(self._reDataSplitValues, data)[1:]

        try:
            m = re.findall(self._reDataVariables, data)
            if m:
                i = 0
                for var in m:
                    variables[var] = vars[i].strip()
                    i = i+1
        except Exception as e:
            self._logger.debug(e)

        self.propDataReveived.emit(variables)

    # __________________________________________________________________
    def closeEvent(self, e):

        self.aboutToClose.emit()

    # __________________________________________________________________
    @pyqtSlot()
    def onConnectedToMqttBroker(self):

        if self._led.color() == 'red':
            self._led.switchOn('yellow')

    # __________________________________________________________________
    @pyqtSlot()
    def onDisconnectedToMqttBroker(self):

        self._led.switchOn('red')

    # __________________________________________________________________
    @pyqtSlot(str, str)
    def onMessageReceived(self, topic, message):

        if message.startswith("DISCONNECTED"):
            self._led.switchOn('yellow')
        else:
            if self._led.color() != 'green':
                self._led.switchOn('green')

        if topic == self._propOutbox and message.startswith('DATA '):
            self._parsePropData(message)

    # __________________________________________________________________
    @pyqtSlot()
    def onSettingsButton(self):

        dlg = PanelSettingsDialog(self._settings, self._logger)
        dlg.setModal(True)
        dlg.move(self.pos() + QPoint(20, 20))
        dlg.exec()

        with open('settings.ini', 'w') as configfile:
            self._settings.write(configfile)

