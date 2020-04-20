#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PanelApplet.py
MIT License (c) Marie Faure <dev at faure dot systems>

PanelApplet application extends MqttApplet.
"""

from constants import *
from MqttApplet import MqttApplet
from PanelDialog import PanelDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class PanelApplet(MqttApplet):

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):
        super().__init__(argv, client, debugging_mqtt)

        self.setApplicationDisplayName(APPDISPLAYNAME)

        self._PanelDialog = PanelDialog(self.tr("Example"), './mqtticon.png',
                                          self._definitions['mqtt-sub-prop'], self._logger)
        self._PanelDialog.aboutToClose.connect(self.exitOnClose)
        self._PanelDialog.publishMessage.connect(self.publishMessage)

        self.connectedToMqttBroker.connect(self._PanelDialog.onConnectedToMqttBroker)
        self.disconnectedToMqttBroker.connect(self._PanelDialog.onDisconnectedToMqttBroker)
        self.messageReceived.connect(self._PanelDialog.onMessageReceived)

        self._PanelDialog.show()

    # __________________________________________________________________
    @pyqtSlot()
    def exitOnClose(self):
        self._logger.info(self.tr("exitOnClose "))
        self.quit()
