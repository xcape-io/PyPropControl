#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PluginApplet.py
MIT License (c) Marie Faure <dev at faure dot systems>

PluginApplet application extends MqttApplet.
"""

from constants import *
from MqttApplet import MqttApplet
from PluginDialog import PluginDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class PluginApplet(MqttApplet):

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):
        super().__init__(argv, client, debugging_mqtt)

        self.setApplicationDisplayName(APPDISPLAYNAME)

        self._PluginDialog = PluginDialog(self.tr("Plugin"), './room.png',
                                          self._definitions['mqtt-sub-prop'], self._logger)
        self._PluginDialog.aboutToClose.connect(self.exitOnClose)
        self._PluginDialog.publishMessage.connect(self.publishMessage)

        self.connectedToMqttBroker.connect(self._PluginDialog.onConnectedToMqttBroker)
        self.disconnectedToMqttBroker.connect(self._PluginDialog.onDisconnectedToMqttBroker)
        self.messageReceived.connect(self._PluginDialog.onMessageReceived)

        self._PluginDialog.show()

    # __________________________________________________________________
    @pyqtSlot()
    def exitOnClose(self):
        self._logger.info(self.tr("exitOnClose "))
        self.quit()
